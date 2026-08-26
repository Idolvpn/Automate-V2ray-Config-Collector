from dataclasses import dataclass, field
from typing import Optional

from src.models.protocol import Protocol


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
        return f"{self.protocol}:{self.host}:{self.port}:{self._credential_fingerprint()}"

    def _credential_fingerprint(self) -> str:
        # Subclasses of the raw string before the remark/fragment are what
        # actually matter for identity; strip the "#remark" portion.
        return self.raw.split("#", 1)[0]

    def renamed(self, remark: str) -> str:
        """Return the raw config string with its remark replaced."""
        base = self.raw.split("#", 1)[0]
        return f"{base}#{remark}"
