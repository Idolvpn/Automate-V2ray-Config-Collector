import json
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

from src.models.protocol import Protocol
from src.utils.encoding import decode_base64


def _normalize_query(query: str) -> str:
    """Sort query params so '?a=1&b=2' and '?b=2&a=1' dedup to the same key."""
    if not query:
        return ""
    try:
        params = parse_qsl(query, keep_blank_values=True)
        params.sort()
        return urlencode(params, doseq=True)
    except Exception:  # noqa: BLE001 - fall back to raw on weird input
        return query


@dataclass
class Config:
    """A single parsed proxy configuration."""

    raw: str
    protocol: Protocol
    host: str
    port: int
    network: str = "tcp"
    source: str = "unknown"

    # Filled in later pipeline stages
    latency_ms: Optional[int] = None
    country: str = "Unknown"
    country_code: str = "UN"

    def identity(self) -> str:
        """A stable key used for deduplication.

        Two configs that point at the same host/port/protocol with the
        same core credentials are considered duplicates even if their
        remark (#name) differs, which is the main dedup gap in most
        collector scripts.
        """
        return f"{self.protocol}:{self.host.lower()}:{self.port}:{self._credential_fingerprint()}"

    def _credential_fingerprint(self) -> str:
        # Part before '#' is what matters; normalize query order and
        # strip vmess 'ps' (display name inside the JSON payload).
        base = self.raw.split("#", 1)[0].strip()
        try:
            if base.startswith("vmess://"):
                payload = decode_base64(base[len("vmess://") :])
                if payload:
                    data = json.loads(payload)
                    data.pop("ps", None)
                    # Normalize JSON key order for a stable fingerprint.
                    normalized = json.dumps(data, sort_keys=True, separators=(",", ":"))
                    return f"vmess://{normalized}"
            parsed = urlparse(base)
            normalized_query = _normalize_query(parsed.query)
            parsed = parsed._replace(query=normalized_query, fragment="")
            return urlunparse(parsed)
        except Exception:  # noqa: BLE001 - never break dedup on odd input
            return base

    def renamed(self, remark: str) -> str:
        """Return the raw config string with its remark replaced (URL-encoded)."""
        base = self.raw.split("#", 1)[0]
        return f"{base}#{quote(remark, safe='')}"
