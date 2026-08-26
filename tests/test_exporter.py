import json
import os

from src.core.exporter import ConfigExporter
from src.models.config import Config
from src.models.protocol import Protocol


def _config(host, protocol, country_code="US"):
    c = Config(
        raw=f"{protocol}://x@{host}:443#{country_code}",
        protocol=protocol,
        host=host,
        port=443,
    )
    c.country_code = country_code
    c.latency_ms = 100
    return c


def test_export_writes_expected_files(tmp_path):
    exporter = ConfigExporter(output_dir=str(tmp_path))
    configs = [
        _config("1.1.1.1", Protocol.VLESS, "US"),
        _config("2.2.2.2", Protocol.TROJAN, "DE"),
    ]
    exporter.export(configs)

    assert os.path.exists(tmp_path / "mix.txt")
    assert os.path.exists(tmp_path / "mix_sub.txt")
    assert os.path.exists(tmp_path / "vless.txt")
    assert os.path.exists(tmp_path / "trojan.txt")
    assert os.path.exists(tmp_path / "stats.json")

    stats = json.loads((tmp_path / "stats.json").read_text())
    assert stats["total"] == 2


def test_export_overwrites_not_appends(tmp_path):
    exporter = ConfigExporter(output_dir=str(tmp_path))
    exporter.export([_config("1.1.1.1", Protocol.VLESS)])
    exporter.export([_config("2.2.2.2", Protocol.VLESS)])

    content = (tmp_path / "vless.txt").read_text()
    assert "1.1.1.1" not in content
    assert "2.2.2.2" in content
