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


def load_settings() -> Settings:
    """Load runtime settings from environment variables with sane defaults.

    Every tunable knob lives here instead of being hardcoded across the
    codebase, so behavior can be adjusted per-environment (CI vs local)
    without touching source files.
    """
    return Settings(
        max_workers=_int_env("MAX_WORKERS", 30),
        fetch_timeout=_float_env("FETCH_TIMEOUT", 15),
        ping_timeout=_float_env("PING_TIMEOUT", 2.0),
        ping_retries=_int_env("PING_RETRIES", 1),
        latency_threshold_ms=_int_env("LATENCY_THRESHOLD_MS", 2000),
        telegram_messages_per_channel=_int_env("TELEGRAM_MESSAGES_PER_CHANNEL", 20),
        geoip_enabled=_bool_env("GEOIP_ENABLED", True),
        geoip_cache_ttl_seconds=_int_env("GEOIP_CACHE_TTL_SECONDS", 86400),
        output_dir=os.environ.get("OUTPUT_DIR", "configs"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
