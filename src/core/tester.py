import json
import os
import socket
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional

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


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _tcp_check(host: str, port: int, timeout: float = 2.0) -> bool:
    """Fast TCP pre-filter before spinning up xray."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _test_single_config(config: Config, timeout: float) -> Optional[int]:
    """
    Real health check using xray-core.
    Returns latency in ms if the proxy can actually forward HTTP traffic,
    otherwise None.
    """
    # 1. Quick TCP pre-filter — skip xray overhead for dead hosts
    if not _tcp_check(config.host, config.port):
        return None

    # 2. Build xray JSON config
    local_port = find_free_port()
    xray_cfg = build_xray_config(config, local_port)
    if not xray_cfg:
        return None

    cfg_path = ""
    proc = None
    try:
        # Write temp config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(xray_cfg, f)
            cfg_path = f.name

        # Start xray-core
        proc = subprocess.Popen(
            [XRAY_BIN, "-c", cfg_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(XRAY_STARTUP_DELAY)

        # 3. Test HTTP through the local SOCKS5 proxy
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

        # Accept 200/204 (direct OK) and 301/302 (CDN redirect — still alive)
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
    """Tests configs with real xray-core proxy validation."""

    def __init__(self, timeout: float, retries: int, threshold_ms: int, max_workers: int):
        self.timeout = timeout
        self.retries = retries
        self.threshold_ms = threshold_ms
        self.max_workers = max_workers

    def test_all(self, configs: Iterable[Config]) -> List[Config]:
        configs = list(configs)
        healthy: List[Config] = []

        logger.info(
            "Real health check starting for %d configs (workers=%d, timeout=%.1fs)",
            len(configs),
            self.max_workers,
            self.timeout,
        )

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_config = {
                pool.submit(_test_single_config, c, self.timeout): c
                for c in configs
            }
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                latency = future.result()

                # Retry logic
                if latency is None and self.retries > 0:
                    for _ in range(self.retries):
                        latency = _test_single_config(config, self.timeout)
                        if latency is not None:
                            break

                if latency is not None and latency < self.threshold_ms:
                    config.latency_ms = latency
                    healthy.append(config)

        logger.info(
            "Real health check complete: %d/%d configs passed (threshold=%dms)",
            len(healthy),
            len(configs),
            self.threshold_ms,
        )
        return healthy
