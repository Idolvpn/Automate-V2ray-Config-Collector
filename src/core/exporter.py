import json
import os
from collections import defaultdict
from typing import Dict, List

from src.models.config import Config
from src.utils.encoding import encode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigExporter:
    """Writes final config lists to disk, grouped several different ways.

    Every write replaces the file's full contents instead of appending,
    so re-running the collector never accumulates stale duplicates the
    way a naive `appendFile` loop would.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.max_configs = 0

    def export(self, configs: List[Config]) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

        by_protocol: Dict[str, List[Config]] = defaultdict(list)
        by_country: Dict[str, List[Config]] = defaultdict(list)
        by_network: Dict[str, List[Config]] = defaultdict(list)

        for config in configs:
            by_protocol[str(config.protocol)].append(config)
            by_country[config.country_code].append(config)
            by_network[config.network].append(config)

        for protocol, group in by_protocol.items():
            self._write_group(f"{protocol}.txt", group)

        for country_code, group in by_country.items():
            if country_code and country_code != "UN":
                self._write_group(f"country_{country_code}.txt", group)

        for network, group in by_network.items():
            self._write_group(f"network_{network}.txt", group)

        self._write_group("mix.txt", configs)
        self._write_subscription("mix_sub.txt", configs)
        self._write_lite_mix(configs)
        self._write_stats(configs, by_protocol, by_country)

        logger.info("Exported %d configs to %s", len(configs), self.output_dir)

    def _write_group(self, filename: str, configs: List[Config]) -> None:
        path = os.path.join(self.output_dir, filename)
        content = "\n".join(c.raw for c in configs)
        self._atomic_write(path, content)

    def _write_subscription(self, filename: str, configs: List[Config]) -> None:
        path = os.path.join(self.output_dir, filename)
        joined = "\n".join(c.raw for c in configs)
        self._atomic_write(path, encode_base64(joined))

    def _write_lite_mix(self, configs: List[Config]) -> None:
        """Write a lite version of mix with max N configs."""
        if self.max_configs <= 0:
            return

        lite_configs = configs[:self.max_configs]
        self._write_group("lite_mix.txt", lite_configs)
        self._write_subscription("lite_mix_sub.txt", lite_configs)
        logger.info(
            "Exported lite mix: %d configs (max %d)",
            len(lite_configs),
            self.max_configs,
        )

    def _write_stats(
        self,
        configs: List[Config],
        by_protocol: Dict[str, List[Config]],
        by_country: Dict[str, List[Config]],
    ) -> None:
        stats = {
            "total": len(configs),
            "by_protocol": {k: len(v) for k, v in by_protocol.items()},
            "by_country": {k: len(v) for k, v in by_country.items()},
            "avg_latency_ms": self._avg_latency(configs),
        }
        path = os.path.join(self.output_dir, "stats.json")
        self._atomic_write(path, json.dumps(stats, indent=2, ensure_ascii=False))

    @staticmethod
    def _avg_latency(configs: List[Config]) -> float:
        latencies = [c.latency_ms for c in configs if c.latency_ms is not None]
        if not latencies:
            return 0.0
        return round(sum(latencies) / len(latencies), 1)

    @staticmethod
    def _atomic_write(path: str, content: str) -> None:
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
