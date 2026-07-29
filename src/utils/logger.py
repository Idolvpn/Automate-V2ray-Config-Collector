import logging
import os
import sys


def setup_logger(name: str) -> logging.Logger:
    """Create a module-level logger honoring LOG_LEVEL from the environment.

    Centralizing this avoids the pattern seen in many collector scripts
    where errors are silently swallowed (bare `except: pass`) with no
    trace of what actually failed.
    """
    logger = logging.getLogger(name)
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
