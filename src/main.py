import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import load_settings  # noqa: E402
from src.core.collector import Collector  # noqa: E402
from src.core.exporter import ConfigExporter  # noqa: E402
from src.core.fetcher import Fetcher  # noqa: E402
from src.core.geoip import GeoIPResolver  # noqa: E402
from src.core.notifier import TelegramNotifier  # noqa: E402
from src.core.tester import ConfigTester  # noqa: E402
from src.utils.logger import setup_logger  # noqa: E402

logger = setup_logger(__name__)


def main() -> None:
    settings = load_settings()

    fetcher = Fetcher(timeout=settings.fetch_timeout, max_workers=settings.max_workers)
    tester = ConfigTester(
        timeout=settings.ping_timeout,
        retries=settings.ping_retries,
        threshold_ms=settings.latency_threshold_ms,
        max_workers=settings.max_workers,
    )
    geoip = GeoIPResolver(
        enabled=settings.geoip_enabled, cache_ttl_seconds=settings.geoip_cache_ttl_seconds
    )
    exporter = ConfigExporter(output_dir=settings.output_dir)
    exporter.max_configs = settings.max_configs_per_output
    notifier = TelegramNotifier(
        token=os.environ.get("TELEGRAM_TOKEN"),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
    )

    collector = Collector(
        fetcher=fetcher,
        tester=tester,
        geoip=geoip,
        exporter=exporter,
        messages_per_channel=settings.telegram_messages_per_channel,
    )

    logger.info("Starting collection run")
    configs = collector.run()
    notifier.send_summary(configs)
    logger.info("Collection run complete: %d healthy configs", len(configs))


if __name__ == "__main__":
    main()
