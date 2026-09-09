import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional, Tuple

import requests

from src.core.xray_builder import build_xray_config
from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) == 0


def _wait_for_port(port: int, timeout: float) -> bool:
    deadline = time.perf_counter() + timeout
    while time.perf_counter() < deadline:
        if _is_port_open(port):
            return True
        time.sleep(0.1)
    return False


def _tcp_connect_latency(host: str, port: int, timeout: float) -> Optional[int]:
    """Fast TCP connect + latency measurement."""
    try:
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=timeout):
            return int((time.perf_counter() - start) * 1000)
    except OSError:
        return None


class ConfigTester:
    """Two-stage health checker: fast TCP filter -> real xray validation."""

    def __init__(
        self,
        timeout: float,
        retries: int,
        threshold_ms: int,
        max_workers: int,
        xray_path: Optional[str] = None,
        test_url: Optional[str] = None,
        xray_startup_delay: float = 2.0,
        tcp_filter_limit: int = 2000,
        tcp_filter_workers: int = 100,
        tcp_filter_timeout: float = 3.0,
    ):
        self.timeout = timeout
        self.retries = retries
        self.threshold_ms = threshold_ms
        self.max_workers = max_workers
        # Fall back to env so old call sites keep working, but instance
        # attributes are the single source of truth (no import-time globals).
        self.xray_path = xray_path or os.environ.get("XRAY_PATH", "xray")
        self.test_url = test_url or os.environ.get(
            "TEST_URL", "http://cp.cloudflare.com"
        )
        self.xray_startup_delay = xray_startup_delay
        self.tcp_filter_limit = tcp_filter_limit
        self.tcp_filter_workers = tcp_filter_workers
        self.tcp_filter_timeout = tcp_filter_timeout
        self._xray_missing_warned = False

    def _xray_available(self) -> bool:
        # Absolute/relative path with separator: check file directly,
        # otherwise resolve via PATH.
        if os.sep in self.xray_path or (
            os.altsep and os.altsep in self.xray_path
        ):
            ok = os.path.isfile(self.xray_path) and os.access(
                self.xray_path, os.X_OK
            )
        else:
            ok = shutil.which(self.xray_path) is not None
        if not ok and not self._xray_missing_warned:
            logger.warning(
                "Xray binary not found: %s. All xray health checks will fail. "
                "Install xray-core to enable real validation.",
                self.xray_path,
            )
            self._xray_missing_warned = True
        return ok

    def _fast_tcp_filter(self, configs: List[Config]) -> List[Config]:
        """
        Stage 1: High-concurrency TCP handshake filter.
        Returns only the top N fastest configs by TCP latency.
        """
        if self.tcp_filter_limit <= 0 or len(configs) <= self.tcp_filter_limit:
            return configs

        logger.info(
            "Stage 1 - TCP fast filter: testing %d configs (workers=%d, timeout=%.1fs)",
            len(configs),
            self.tcp_filter_workers,
            self.tcp_filter_timeout,
        )

        results: List[Tuple[Config, Optional[int]]] = []

        with ThreadPoolExecutor(max_workers=self.tcp_filter_workers) as pool:
            future_to_config = {
                pool.submit(
                    _tcp_connect_latency, c.host, c.port, self.tcp_filter_timeout
                ): c
                for c in configs
            }
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    latency = future.result()
                except Exception:  # noqa: BLE001 - never fail the batch
                    latency = None
                results.append((config, latency))

        # Sort by latency (None = dead, goes to bottom), keep top N
        alive = [(c, lat) for c, lat in results if lat is not None]
        alive.sort(key=lambda x: x[1])
        top = [c for c, _ in alive[: self.tcp_filter_limit]]
        logger.info(
            "Stage 1 complete: %d/%d alive, keeping top %d for real xray test",
            len(alive),
            len(configs),
            len(top),
        )
        return top

    def _test_single_config(self, config: Config) -> Optional[int]:
        """
        Stage 2: Real health check using xray-core.
        Returns latency in ms if the proxy can actually forward HTTP traffic.
        """
        xray_cfg = build_xray_config(config, 0)  # port patched below
        if not xray_cfg:
            # Unsupported protocol (e.g. wireguard): skip without spawning xray.
            return None

        if not self._xray_available():
            return None

        cfg_path = ""
        proc = None
        # Retry with a fresh port if xray fails to bind (TOCTOU race on
        # find_free_port under high concurrency).
        for _ in range(3):
            local_port = find_free_port()
            xray_cfg["inbounds"][0]["port"] = local_port
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".json", delete=False
                ) as f:
                    json.dump(xray_cfg, f)
                    cfg_path = f.name

                proc = subprocess.Popen(
                    [self.xray_path, "-c", cfg_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if not _wait_for_port(local_port, self.xray_startup_delay):
                    # Xray didn't listen in time: crashed or port taken.
                    # Clean up and try another port.
                    self._stop_proc(proc)
                    proc = None
                    self._rm_file(cfg_path)
                    cfg_path = ""
                    continue

                start = time.perf_counter()
                proxies = {
                    "http": f"socks5://127.0.0.1:{local_port}",
                    "https": f"socks5://127.0.0.1:{local_port}",
                }
                resp = requests.get(
                    self.test_url,
                    proxies=proxies,
                    timeout=self.timeout,
                    allow_redirects=False,
                )
                elapsed = int((time.perf_counter() - start) * 1000)

                if resp.status_code in (200, 204, 301, 302):
                    # Guard against a malicious/broken exit node that
                    # returns 200 for everything: the default test URL
                    # (cp.cloudflare.com) must contain "success" in body.
                    if resp.status_code == 200 and "cp.cloudflare.com" in self.test_url:
                        try:
                            body = (resp.content or b"")[:2048].lower()
                        except Exception:  # noqa: BLE001
                            return None
                        if b"success" not in body:
                            return None
                    return elapsed
                return None

            except FileNotFoundError:
                # Xray binary disappeared between check and exec.
                self._xray_available()
                return None
            except Exception:
                return None
            finally:
                if proc:
                    self._stop_proc(proc)
                    proc = None
                if cfg_path:
                    self._rm_file(cfg_path)
                    cfg_path = ""
        return None

    @staticmethod
    def _stop_proc(proc: "subprocess.Popen") -> None:
        try:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
        except Exception:  # noqa: BLE001
            pass

    @staticmethod
    def _rm_file(path: str) -> None:
        try:
            os.unlink(path)
        except OSError:
            pass

    def test_all(self, configs: Iterable[Config]) -> List[Config]:
        configs = list(configs)

        # Stage 1: Fast TCP filter (high concurrency)
        candidates = self._fast_tcp_filter(configs)

        if not candidates:
            logger.warning("No configs survived TCP fast filter.")
            return []

        # Stage 2: Real xray test (lower concurrency)
        logger.info(
            "Stage 2 - Real xray test: %d configs (workers=%d, timeout=%.1fs)",
            len(candidates),
            self.max_workers,
            self.timeout,
        )

        healthy: List[Config] = []
        done = 0
        total = len(candidates)
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_config = {
                pool.submit(self._test_single_config, c): c for c in candidates
            }
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    latency = future.result()
                except Exception:  # noqa: BLE001
                    latency = None

                if latency is None and self.retries > 0:
                    for _ in range(self.retries):
                        latency = self._test_single_config(config)
                        if latency is not None:
                            break

                if latency is not None and latency <= self.threshold_ms:
                    config.latency_ms = latency
                    healthy.append(config)

                done += 1
                if done % 50 == 0 or done == total:
                    logger.info(
                        "Stage 2 progress: %d/%d tested, %d healthy so far",
                        done,
                        total,
                        len(healthy),
                    )

        logger.info(
            "Health check complete: %d/%d passed xray real test (threshold=%dms)",
            len(healthy),
            len(candidates),
            self.threshold_ms,
        )
        return healthy
