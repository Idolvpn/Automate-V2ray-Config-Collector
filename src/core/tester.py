import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional

from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def _resolve(host: str, port: int):
    try:
        return socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror:
        return []


def _connect_latency(host: str, port: int, timeout: float, retries: int) -> Optional[int]:
    """Return TCP connection latency in ms, or None if unreachable.

    A successful TCP handshake doesn't guarantee the proxy protocol itself
    works, but it's a cheap, dependency-free first filter that catches the
    majority of dead configs before they ever reach the output files.
    """
    addresses = _resolve(host, port)
    if not addresses:
        return None
    for attempt in range(retries + 1):
        for family, socktype, proto, _, sockaddr in addresses:
            start = time.perf_counter()
            try:
                with socket.socket(family, socktype, proto) as sock:
                    sock.settimeout(timeout)
                    sock.connect(sockaddr)
                return int((time.perf_counter() - start) * 1000)
            except (socket.timeout, OSError):
                continue
    return None


class ConfigTester:
    """Tests configs for TCP reachability concurrently."""

    def __init__(self, timeout: float, retries: int, threshold_ms: int, max_workers: int):
        self.timeout = timeout
        self.retries = retries
        self.threshold_ms = threshold_ms
        self.max_workers = max_workers

    def test_all(self, configs: Iterable[Config]) -> List[Config]:
        """Return only the configs that responded within the latency threshold."""
        configs = list(configs)
        healthy: List[Config] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_config = {
                pool.submit(
                    _connect_latency, c.host, c.port, self.timeout, self.retries
                ): c
                for c in configs
            }
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                latency = future.result()
                if latency is not None and latency < self.threshold_ms:
                    config.latency_ms = latency
                    healthy.append(config)

        logger.info(
            "Health check: %d/%d configs reachable (threshold=%dms)",
            len(healthy),
            len(configs),
            self.threshold_ms,
        )
        return healthy
