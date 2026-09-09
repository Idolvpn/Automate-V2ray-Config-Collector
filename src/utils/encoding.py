import base64
from typing import Optional


def decode_base64(data: str) -> Optional[str]:
    """Decode a (possibly unpadded / urlsafe) base64 string to UTF-8 text.

    Returns None instead of raising, since collector code deals with a lot
    of malformed/truncated input scraped from the wild.
    """
    if not data:
        return None
    cleaned = data.strip().replace("-", "+").replace("_", "/")
    # Reject strings with characters outside the base64 alphabet instead
    # of silently ignoring errors (which could turn an HTML error page
    # into garbage that later matches the config regex).
    stripped = cleaned.rstrip("=")
    import re as _re

    if _re.search(r"[^A-Za-z0-9+/]", stripped):
        return None
    padding = len(cleaned) % 4
    if padding:
        cleaned += "=" * (4 - padding)
    try:
        return base64.b64decode(cleaned, validate=True).decode("utf-8")
    except (base64.binascii.Error, ValueError, UnicodeDecodeError):
        return None


def encode_base64(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("ascii")
