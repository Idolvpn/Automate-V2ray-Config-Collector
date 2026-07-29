import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List

import requests

from src.utils.encoding import decode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

CONFIG_LINE_RE = re.compile(
    r"(?:vmess|vless|trojan|ss|wireguard)://[^\s<>\"'\\]+", re.IGNORECASE
)

# Telegram preview pages HTML-escape config strings; only the entities that
# actually show up in proxy URLs need unescaping.
_HTML_ENTITIES = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#039;": "'",
}


def _unescape_html(text: str) -> str:
    for entity, char in _HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text


def extract_configs(text: str) -> List[str]:
    """Pull every recognizable config URI out of a blob of text/HTML."""
    if not text:
        return []
    matches = CONFIG_LINE_RE.findall(text)
    cleaned = []
    for match in matches:
        unescaped = _unescape_html(match)
        # Telegram truncates long messages with an ellipsis; a truncated
        # config is worse than useless (silently fails at connect time),
        # so drop anything that looks cut off.
        if "…" in unescaped or unescaped.endswith("..."):
            continue
        cleaned.append(unescaped)
    return cleaned


class Fetcher:
    """Fetches raw subscription sources and Telegram channel previews."""

    def __init__(self, timeout: float, max_workers: int):
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; V2RayCollector/1.0)"}
        )

    def fetch_raw_sources(self, urls: Iterable[str]) -> dict[str, List[str]]:
        """Fetch plain/base64 subscription URLs. Returns {url: [config,...]}."""
        results: dict[str, List[str]] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_url = {
                pool.submit(self._fetch_one_raw_source, url): url for url in urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as exc:  # noqa: BLE001 - log and continue
                    logger.warning("Failed to fetch source %s: %s", url, exc)
                    results[url] = []
        return results

    def _fetch_one_raw_source(self, url: str) -> List[str]:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        body = response.text.strip()

        configs = extract_configs(body)
        if configs:
            return configs

        # No direct matches -- this source is probably a base64 blob.
        decoded = decode_base64(body)
        if decoded:
            return extract_configs(decoded)

        logger.info("Source returned no usable configs: %s", url)
        return []

    def fetch_telegram_channels(
        self, channels: Iterable[str], messages_per_channel: int
    ) -> dict[str, List[str]]:
        """Fetch recent configs from public Telegram channel previews."""
        results: dict[str, List[str]] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_channel = {
                pool.submit(
                    self._fetch_one_channel, channel, messages_per_channel
                ): channel
                for channel in channels
            }
            for future in as_completed(future_to_channel):
                channel = future_to_channel[future]
                try:
                    results[channel] = future.result()
                except Exception as exc:  # noqa: BLE001 - log and continue
                    logger.warning("Failed to fetch channel %s: %s", channel, exc)
                    results[channel] = []
        return results

    def _fetch_one_channel(self, channel: str, limit: int) -> List[str]:
        url = f"https://t.me/s/{channel}"
        response = self.session.get(url, timeout=self.timeout)
        if response.status_code != 200:
            logger.info("Telegram channel unavailable (%s): %s", response.status_code, channel)
            return []

        configs = extract_configs(response.text)
        if not configs:
            logger.info("No configs found in channel: %s", channel)
            return []

        # Keep the most recent N matches instead of just the last 2 --
        # channel preview pages list ~20 messages, so this captures far
        # more usable configs per fetch than a hardcoded slice(-2).
        return configs[-limit:]
