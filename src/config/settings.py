import os
from dataclasses import dataclass


def _int_env(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


def _float_env(key: str, default: float) -> float:
    try:
        return float(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


def _bool_env(key: str, default: bool) -> bool:
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    max_workers: int
    fetch_timeout: float
    ping_timeout: float
    ping_retries: int
    latency_threshold_ms: int
    telegram_messages_per_channel: int
    geoip_enabled: bool
    geoip_cache_ttl_seconds: int
    output_dir: str
    log_level: str
    max_configs_per_output: int
    # --- Real health-check additions ---
    xray_path: str
    test_url: str
    xray_startup_delay: float
    # --- Two-stage filter ---
    tcp_filter_limit: int
    tcp_filter_workers: int
    tcp_filter_timeout: float


def load_settings() -> Settings:
    """Load runtime settings from environment variables with sane defaults."""
    return Settings(
        max_workers=_int_env("MAX_WORKERS", 8),
        fetch_timeout=_float_env("FETCH_TIMEOUT", 15),
        ping_timeout=_float_env("PING_TIMEOUT", 8.0),
        ping_retries=_int_env("PING_RETRIES", 1),
        latency_threshold_ms=_int_env("LATENCY_THRESHOLD_MS", 5000),
        telegram_messages_per_channel=_int_env("TELEGRAM_MESSAGES_PER_CHANNEL", 20),
        geoip_enabled=_bool_env("GEOIP_ENABLED", True),
        geoip_cache_ttl_seconds=_int_env("GEOIP_CACHE_TTL_SECONDS", 86400),
        output_dir=os.environ.get("OUTPUT_DIR", "configs"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        max_configs_per_output=_int_env("MAX_CONFIGS_PER_OUTPUT", 0),
        xray_path=os.environ.get("XRAY_PATH", "xray"),
        test_url=os.environ.get("TEST_URL", "http://cp.cloudflare.com"),
        xray_startup_delay=_float_env("XRAY_STARTUP_DELAY", 1.5),
        # Two-stage filter defaults
        tcp_filter_limit=_int_env("TCP_FILTER_LIMIT", 2000),
        tcp_filter_workers=_int_env("TCP_FILTER_WORKERS", 100),
        tcp_filter_timeout=_float_env("TCP_FILTER_TIMEOUT", 2.0),
    )
