from typing import Iterable, List

from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def deduplicate(configs: Iterable[Config]) -> List[Config]:
    """Remove duplicate configs by identity (protocol+host+port+credentials).

    None of the three reference projects this was built from de-duplicate
    across runs or across sources -- files just grow with repeated
    entries every cycle. This keeps the first-seen config per identity
    and drops the rest.
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
