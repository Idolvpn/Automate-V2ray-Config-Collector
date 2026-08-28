import json
import os
import socket
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional, Tuple

import requests

from src.config.settings import load_settings
from src.core.xray_builder import build_xray_config
from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
settings = load_settings()

XRAY_BIN = os.environ.get("XRAY_PATH", "xray")
TEST_URL = os.environ.get("TEST_URL", "http://cp.cloudflare.com")
XRAY_STARTUP_DELAY = settings.xray_startup_delay
TCP_FILTER_LIMIT = settings.tcp_filter_limit
TCP_FILTER_WORKERS = settings.tcp_filter_workers
TCP_FILTER_TIMEOUT = settings.tcp_filter_timeout


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _tcp_connect_latency(host: str, port: int, timeout: float) -> Optional[int]:
    """Fast TCP connect + latency measurement."""
    try:
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=timeout):
            return int((time.perf_counter() - start) * 1000)
    except OSError:
        return None


def _fast_tcp_filter(configs: List[Config]) -> List[Config]:
    """
    Stage 1: High-concurrency TCP handshake filter.
    Returns only the top N fastest configs by TCP latency.
    """
    if TCP_FILTER_LIMIT <= 0 or len(configs) <= TCP_FILTER_LIMIT:
        return configs

    logger.info(
        "Stage 1 — TCP fast filter: testing %d configs (workers=%d, timeout=%.1fs)",
        len(configs),
        TCP_FILTER_WORKERS,
        TCP_FILTER_TIMEOUT,
    )

    results: List[Tuple[Config, Optional[int]]] = []

    with ThreadPoolExecutor(max_workers=TCP_FILTER_WORKERS) as pool:
        future_to_config = {
            pool.submit(_tcp_connect_latency, c.host, c.port, TCP_FILTER_TIMEOUT): c
            for c in configs
        }
        for future in as_completed(future_to_config):
            config = future_to_config[future]
            latency = future.result()
            results.append((config, latency))

    # Sort by latency (None = dead, goes to bottom), keep top N
    alive = [(c, lat) for c, lat in results if lat is not None]
    alive.sort(key=lambda x: x[1])
    top = [c for c, _ in alive[:TCP_FILTER_LIMIT]]

    logger.info(
        "Stage 1 complete: %d/%d alive, keeping top %d for real xray test",
        len(alive),
        len(configs),
        len(top),
    )
    return top


def _test_single_config(config: Config, timeout: float) -> Optional[int]:
    """
    Stage 2: Real health check using xray-core.
    Returns latency in ms if the proxy can actually forward HTTP traffic.
    """
    local_port = find_free_port()
    xray_cfg = build_xray_config(config, local_port)
    if not xray_cfg:
        return None

    cfg_path = ""
    proc = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(xray_cfg, f)
            cfg_path = f.name

        proc = subprocess.Popen(
            [XRAY_BIN, "-c", cfg_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(XRAY_STARTUP_DELAY)

        start = time.perf_counter()
        proxies = {
            "http": f"socks5://127.0.0.1:{local_port}",
            "https": f"socks5://127.0.0.1:{local_port}",
        }
        resp = requests.get(
            TEST_URL,
            proxies=proxies,
            timeout=timeout,
            allow_redirects=False,
        )
        elapsed = int((time.perf_counter() - start) * 1000)

        if resp.status_code in (200, 204, 301, 302):
            return elapsed
        return None

    except Exception:
        return None
    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
        if cfg_path:
            try:
                os.unlink(cfg_path)
            except OSError:
                pass


class ConfigTester:
    """Two-stage health checker: fast TCP filter → real xray validation."""

    def __init__(self, timeout: float, retries: int, threshold_ms: int, max_workers: int):
        self.timeout = timeout
        self.retries = retries
        self.threshold_ms = threshold_ms
        self.max_workers = max_workers

    def test_all(self, configs: Iterable[Config]) -> List[Config]:
        configs = list(configs)

        # Stage 1: Fast TCP filter (high concurrency)
        candidates = _fast_tcp_filter(configs)

        if not candidates:
            logger.warning("No configs survived TCP fast filter.")
            return []

        # Stage 2: Real xray test (lower concurrency)
        logger.info(
            "Stage 2 — Real xray test: %d configs (workers=%d, timeout=%.1fs)",
            len(candidates),
            self.max_workers,
            self.timeout,
        )

        healthy: List[Config] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_config = {
                pool.submit(_test_single_config, c, self.timeout): c
                for c in candidates
            }
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                latency = future.result()

                if latency is None and self.retries > 0:
                    for _ in range(self.retries):
                        latency = _test_single_config(config, self.timeout)
                        if latency is not None:
                            break

                if latency is not None and latency < self.threshold_ms:
                    config.latency_ms = latency
                    healthy.append(config)

        logger.info(
            "Health check complete: %d/%d passed xray real test (threshold=%dms)",
            len(healthy),
            len(candidates),
            self.threshold_ms,
        )
        return healthy
