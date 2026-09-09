import json
import os
import time
from typing import Dict, List, Optional, Tuple

import requests

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# ip-api.com's free batch endpoint: up to 100 IPs per request, ~15 req/min.
# Using the batch endpoint instead of one request per config (as the
# reference telegram-collector does) turns hundreds of HTTP calls into a
# handful, and avoids hammering a single undocumented third-party API.
BATCH_URL = "http://ip-api.com/batch"
BATCH_SIZE = 100
MAX_RETRIES = 2


class GeoIPResolver:
    """Resolves IP/host -> country with an in-memory + file TTL cache."""

    def __init__(
        self,
        enabled: bool,
        cache_ttl_seconds: int,
        timeout: float = 10.0,
        cache_file: Optional[str] = None,
    ):
        self.enabled = enabled
        self.cache_ttl = cache_ttl_seconds
        self.timeout = timeout
        self.cache_file = cache_file
        self._cache: Dict[str, Tuple[float, dict]] = {}
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; V2RayCollector/1.0)"}
        )
        if cache_file:
            self._load_file_cache()

    def resolve_many(self, hosts: List[str]) -> Dict[str, dict]:
        """Resolve a list of hosts to {country, countryCode, query(ip)}."""
        if not self.enabled:
            return {host: self._unknown() for host in hosts}

        results: Dict[str, dict] = {}
        to_fetch = []
        now = time.time()

        for host in dict.fromkeys(hosts):  # de-dup while preserving order
            if not host:
                continue
            cached = self._cache.get(host)
            if cached and now - cached[0] < self.cache_ttl:
                results[host] = cached[1]
            else:
                to_fetch.append(host)

        for i in range(0, len(to_fetch), BATCH_SIZE):
            batch = to_fetch[i : i + BATCH_SIZE]
            # Throttle to stay under ~15 req/min on the free tier.
            if i > 0:
                time.sleep(4)
            for host, info in self._query_batch(batch).items():
                results[host] = info
                self._cache[host] = (now, info)

        # Anything that failed to resolve still gets an entry so downstream
        # code never has to special-case a missing key.
        for host in to_fetch:
            results.setdefault(host, self._unknown())

        if self.cache_file and to_fetch:
            self._save_file_cache()

        return results

    def _load_file_cache(self) -> None:
        try:
            if not self.cache_file or not os.path.exists(self.cache_file):
                return
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            now = time.time()
            loaded = 0
            for host, entry in data.items():
                if not isinstance(entry, dict):
                    continue
                ts = entry.get("_ts", 0)
                if now - ts < self.cache_ttl:
                    self._cache[host] = (
                        ts,
                        {k: v for k, v in entry.items() if not k.startswith("_")},
                    )
                    loaded += 1
            logger.info("GeoIP file cache loaded: %d entries", loaded)
        except Exception as exc:  # noqa: BLE001 - cache is best-effort
            logger.warning("GeoIP cache load failed: %s", exc)

    def _save_file_cache(self) -> None:
        try:
            if not self.cache_file:
                return
            os.makedirs(os.path.dirname(self.cache_file) or ".", exist_ok=True)
            data = {
                host: {"_ts": ts, **info} for host, (ts, info) in self._cache.items()
            }
            tmp = self.cache_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            os.replace(tmp, self.cache_file)
        except Exception as exc:  # noqa: BLE001 - cache is best-effort
            logger.warning("GeoIP cache save failed: %s", exc)

    def _query_batch(self, hosts: List[str]) -> Dict[str, dict]:
        payload = [
            {"query": h, "fields": "status,message,country,countryCode,query"}
            for h in hosts
        ]
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = self.session.post(
                    BATCH_URL,
                    json=payload,
                    timeout=self.timeout,
                )
                if response.status_code == 429:
                    wait = 5 * (attempt + 1)
                    logger.warning(
                        "GeoIP rate-limited (429), waiting %ds (attempt %d/%d)",
                        wait,
                        attempt + 1,
                        MAX_RETRIES + 1,
                    )
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                data = response.json()
                break
            except (requests.RequestException, ValueError) as exc:
                logger.warning(
                    "GeoIP batch lookup failed for %d hosts: %s", len(hosts), exc
                )
                if attempt < MAX_RETRIES:
                    time.sleep(2 * (attempt + 1))
                    continue
                return {}
        else:
            return {}

        if not isinstance(data, list):
            logger.warning("GeoIP unexpected response type: %r", type(data))
            return {}

        results: Dict[str, dict] = {}
        for host, entry in zip(hosts, data):
            if not isinstance(entry, dict):
                continue
            if entry.get("status") == "success":
                code = str(entry.get("countryCode", "UN")).upper()[:2] or "UN"
                if len(code) != 2 or not code.isalpha():
                    code = "UN"
                results[host] = {
                    "country": entry.get("country", "Unknown"),
                    "countryCode": code,
                    "ip": entry.get("query", host),
                }
            else:
                logger.debug(
                    "GeoIP lookup failed for %s: %s",
                    host,
                    entry.get("message", "unknown"),
                )
        return results

    @staticmethod
    def _unknown() -> dict:
        return {"country": "Unknown", "countryCode": "UN", "ip": ""}
