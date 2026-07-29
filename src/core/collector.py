from typing import List

from src.config.sources import RAW_SOURCES, TELEGRAM_CHANNELS
from src.core.dedup import deduplicate
from src.core.exporter import ConfigExporter
from src.core.fetcher import Fetcher
from src.core.geoip import GeoIPResolver
from src.core.parser import ConfigParser
from src.core.tester import ConfigTester
from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class Collector:
    """Runs the full pipeline: fetch -> parse -> dedup -> test -> geo-tag -> export."""

    def __init__(
        self,
        fetcher: Fetcher,
        tester: ConfigTester,
        geoip: GeoIPResolver,
        exporter: ConfigExporter,
        messages_per_channel: int,
    ):
        self.fetcher = fetcher
        self.tester = tester
        self.geoip = geoip
        self.exporter = exporter
        self.messages_per_channel = messages_per_channel

    def run(self) -> List[Config]:
        raw_lines = self._fetch_all()
        configs = self._parse_all(raw_lines)
        configs = deduplicate(configs)

        healthy = self.tester.test_all(configs)
        healthy = self._tag_countries(healthy)

        self.exporter.export(healthy)
        return healthy

    def _fetch_all(self) -> List[tuple[str, str]]:
        """Returns a list of (raw_config_line, source_label) tuples."""
        lines: List[tuple[str, str]] = []

        raw_results = self.fetcher.fetch_raw_sources(RAW_SOURCES)
        for url, configs in raw_results.items():
            lines.extend((line, url) for line in configs)

        channel_results = self.fetcher.fetch_telegram_channels(
            TELEGRAM_CHANNELS, self.messages_per_channel
        )
        for channel, configs in channel_results.items():
            lines.extend((line, f"tg:{channel}") for line in configs)

        logger.info("Fetched %d raw config lines from %d sources", len(lines), len(RAW_SOURCES) + len(TELEGRAM_CHANNELS))
        return lines

    def _parse_all(self, raw_lines: List[tuple[str, str]]) -> List[Config]:
        configs = []
        for line, source in raw_lines:
            config = ConfigParser.parse(line, source)
            if config:
                configs.append(config)
        logger.info("Parsed %d valid configs out of %d raw lines", len(configs), len(raw_lines))
        return configs

    def _tag_countries(self, configs: List[Config]) -> List[Config]:
        hosts = [c.host for c in configs]
        geo_info = self.geoip.resolve_many(hosts)

        for config in configs:
            info = geo_info.get(config.host, {})
            config.country = info.get("country", "Unknown")
            config.country_code = info.get("countryCode", "UN")
            ip = info.get("ip") or config.host
            remark = f"{config.country_code} | {ip} | {config.latency_ms}ms"
            config.raw = config.renamed(remark)

        return configs
