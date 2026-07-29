from typing import List, Optional

import requests

from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramNotifier:
    """Sends a short run summary to a Telegram chat, if configured.

    Both token and chat_id are optional -- when either is missing the
    notifier just logs locally instead of raising, so running the
    collector without notification setup never breaks the pipeline.
    """

    def __init__(self, token: Optional[str], chat_id: Optional[str]):
        self.token = token
        self.chat_id = chat_id

    @property
    def enabled(self) -> bool:
        return bool(self.token and self.chat_id)

    def send_summary(self, configs: List[Config]) -> None:
        message = self._build_message(configs)
        if not self.enabled:
            logger.info("Telegram notifier not configured, summary:\n%s", message)
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            response = requests.post(
                url,
                json={"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("Failed to send Telegram notification: %s", exc)

    @staticmethod
    def _build_message(configs: List[Config]) -> str:
        protocols: dict[str, int] = {}
        for config in configs:
            protocols[str(config.protocol)] = protocols.get(str(config.protocol), 0) + 1

        breakdown = "\n".join(f"  {proto}: {count}" for proto, count in sorted(protocols.items()))
        return (
            f"<b>V2Ray Collector run complete</b>\n"
            f"Total healthy configs: {len(configs)}\n"
            f"{breakdown}"
        )
