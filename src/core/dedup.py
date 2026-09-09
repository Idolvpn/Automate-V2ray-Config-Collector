from typing import Iterable, List

from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def deduplicate(configs: Iterable[Config]) -> List[Config]:
    """Remove duplicate configs by identity (protocol+host+port+credentials).

    Keeps the first-seen config per identity and drops the rest, so the
    same server collected from several sources is published only once.
    """
    seen: dict[str, Config] = {}
    total = 0
    for config in configs:
        total += 1
        key = config.identity()
        if key not in seen:
            seen[key] = config

    unique = list(seen.values())
    logger.info("Deduplicated %d configs down to %d", total, len(unique))
    return unique
