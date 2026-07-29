import time
from typing import Dict, List, Tuple

import requests

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# ip-api.com's free batch endpoint: up to 100 IPs per request, ~15 req/min.
# Using the batch endpoint instead of one request per config (as the
# reference telegram-collector does) turns hundreds of HTTP calls into a
# handful, and avoids hammering a single undocumented third-party API.
BATCH_URL = "http://ip-api.com/batch"
BATCH_SIZE = 100


class GeoIPResolver:
    """Resolves IP/host -> country with an in-memory TTL cache."""

    def __init__(self, enabled: bool, cache_ttl_seconds: int, timeout: float = 10.0):
        self.enabled = enabled
        self.cache_ttl = cache_ttl_seconds
        self.timeout = timeout
        self._cache: Dict[str, Tuple[float, dict]] = {}

    def resolve_many(self, hosts: List[str]) -> Dict[str, dict]:
        """Resolve a list of hosts to {country, countryCode, query(ip)}."""
        if not self.enabled:
            return {host: self._unknown() for host in hosts}

        results: Dict[str, dict] = {}
        to_fetch = []
        now = time.time()

        for host in dict.fromkeys(hosts):  # de-dup while preserving order
            cached = self._cache.get(host)
            if cached and now - cached[0] < self.cache_ttl:
                results[host] = cached[1]
            else:
                to_fetch.append(host)

        for batch_start in range(0, len(to_fetch), BATCH_SIZE):
            batch = to_fetch[batch_start : batch_start + BATCH_SIZE]
            for host, info in self._query_batch(batch).items():
                results[host] = info
                self._cache[host] = (now, info)

        # Anything that failed to resolve still gets an entry so downstream
        # code never has to special-case a missing key.
        for host in to_fetch:
            results.setdefault(host, self._unknown())

        return results

    def _query_batch(self, hosts: List[str]) -> Dict[str, dict]:
        try:
            response = requests.post(
                BATCH_URL,
                json=[{"query": h, "fields": "status,country,countryCode,query"} for h in hosts],
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            logger.warning("GeoIP batch lookup failed for %d hosts: %s", len(hosts), exc)
            return {}

        results: Dict[str, dict] = {}
        for host, entry in zip(hosts, data):
            if entry.get("status") == "success":
                results[host] = {
                    "country": entry.get("country", "Unknown"),
                    "countryCode": entry.get("countryCode", "UN"),
                    "ip": entry.get("query", host),
                }
        return results

    @staticmethod
    def _unknown() -> dict:
        return {"country": "Unknown", "countryCode": "UN", "ip": ""}
