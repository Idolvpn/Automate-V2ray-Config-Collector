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
    padding = len(cleaned) % 4
    if padding:
        cleaned += "=" * (4 - padding)
    try:
        return base64.b64decode(cleaned).decode("utf-8", errors="ignore")
    except (base64.binascii.Error, ValueError):
        return None


def encode_base64(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("ascii")
