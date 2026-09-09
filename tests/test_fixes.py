import base64
import json

from src.core.exporter import _sanitize_filename_component
from src.core.fetcher import extract_configs
from src.core.geoip import GeoIPResolver
from src.core.parser import ConfigParser
from src.core.tester import ConfigTester
from src.models.config import Config
from src.models.protocol import Protocol


def test_sanitize_removes_colon_and_traversal():
    assert ":" not in _sanitize_filename_component("tcp:443")
    assert _sanitize_filename_component("tcp:443") == "tcp_443"
    assert "/" not in _sanitize_filename_component("../evil")
    assert _sanitize_filename_component("") == "unknown"


def test_parser_normalizes_bad_network():
    c = ConfigParser.parse("vless://u@example.com:443?type=tcp:443#x")
    assert c is not None
    assert ":" not in c.network


def test_parser_rejects_private_ips():
    assert ConfigParser.parse("vless://u@127.0.0.1:443#x") is None
    assert ConfigParser.parse("trojan://pw@192.168.1.1:443#x") is None
    assert ConfigParser.parse("trojan://pw@10.0.0.1:443#x") is None
    # public IP still accepted
    assert ConfigParser.parse("trojan://pw@8.8.8.8:443#x") is not None


def test_parser_ss_sip002():
    inner = base64.b64encode(b"aes-256-gcm:mypass").decode()
    c = ConfigParser.parse(f"ss://{inner}@9.9.9.9:8388#x")
    assert c is not None
    assert c.host == "9.9.9.9" and c.port == 8388


def test_fetcher_strips_trailing_punct():
    out = extract_configs("see vless://u@h.com:443#n, next")
    assert out == ["vless://u@h.com:443#n"]


def test_dedup_query_order_and_vmess_ps():
    import json as _json

    a = Config(
        raw="trojan://pw@1.1.1.1:443?type=tcp&sni=a#one",
        protocol=Protocol.TROJAN,
        host="1.1.1.1",
        port=443,
    )
    b = Config(
        raw="trojan://pw@1.1.1.1:443?sni=a&type=tcp#two",
        protocol=Protocol.TROJAN,
        host="1.1.1.1",
        port=443,
    )
    assert a.identity() == b.identity()

    def _vmess(ps):
        payload = {"add": "1.2.3.4", "port": 443, "id": "u", "ps": ps}
        enc = base64.b64encode(_json.dumps(payload).encode()).decode()
        return ConfigParser.parse(f"vmess://{enc}")

    assert _vmess("a").identity() == _vmess("b").identity()


def test_renamed_is_url_encoded():
    c = Config(
        raw="trojan://pw@1.1.1.1:443#old",
        protocol=Protocol.TROJAN,
        host="1.1.1.1",
        port=443,
    )
    assert c.renamed("DE | 1.2.3.4 | 10ms").endswith("#DE%20%7C%201.2.3.4%20%7C%2010ms")


def test_exporter_sorts_stale_and_empty(tmp_path):
    from src.core.exporter import ConfigExporter

    def _c(host, ms, cc="US", net="tcp"):
        c = Config(
            raw=f"vless://u@{host}:443#x",
            protocol=Protocol.VLESS,
            host=host,
            port=443,
            network=net,
        )
        c.latency_ms = ms
        c.country_code = cc
        return c

    d = str(tmp_path)
    (tmp_path / "country_XX.txt").write_text("stale")
    exp = ConfigExporter(output_dir=d, max_configs=1)
    exp.export([_c("1.1.1.1", 300, "US"), _c("2.2.2.2", 50, "DE")])
    lines = (tmp_path / "mix.txt").read_text().splitlines()
    assert "2.2.2.2" in lines[0]  # fastest first
    assert not (tmp_path / "country_XX.txt").exists()
    assert len((tmp_path / "lite_mix.txt").read_text().splitlines()) == 1
    stats = json.loads((tmp_path / "stats.json").read_text())
    assert stats["total"] == 2 and "updated_at" in stats and stats["stale"] is False
    # tiny countries skipped
    exp2 = ConfigExporter(output_dir=d)
    exp2.export([_c("3.3.3.3", 10, "FR")])
    assert not (tmp_path / "country_FR.txt").exists()
    # empty export keeps mix but marks stats stale
    exp.export([])
    assert (tmp_path / "mix.txt").exists()
    stats2 = json.loads((tmp_path / "stats.json").read_text())
    assert stats2["total"] == 0 and stats2["stale"] is True


def test_exporter_no_colon_filename(tmp_path):
    from src.core.exporter import ConfigExporter

    c = Config(
        raw="vless://u@1.1.1.1:443#x",
        protocol=Protocol.VLESS,
        host="1.1.1.1",
        port=443,
        network="tcp:443",
    )
    c.latency_ms = 10
    c.country_code = "US"
    ConfigExporter(output_dir=str(tmp_path)).export([c])
    import os

    assert not any(":" in f for f in os.listdir(tmp_path))


def test_tester_di_params():
    t = ConfigTester(
        timeout=5,
        retries=0,
        threshold_ms=8000,
        max_workers=40,
        xray_path="xray",
        test_url="http://cp.cloudflare.com",
        xray_startup_delay=1.2,
        tcp_filter_limit=600,
        tcp_filter_workers=100,
        tcp_filter_timeout=2.0,
    )
    assert t.tcp_filter_limit == 600
    assert t.timeout == 5


def test_tester_missing_xray_fails_closed():
    t = ConfigTester(
        timeout=0.5, retries=0, threshold_ms=2000, max_workers=2,
        xray_path="nonexistent-xray-xyz",
    )
    c = Config(
        raw="trojan://pw@8.8.8.8:443#x",
        protocol=Protocol.TROJAN,
        host="8.8.8.8",
        port=443,
    )
    assert t.test_all([c]) == []


def test_geoip_file_cache_roundtrip(tmp_path):
    cache = str(tmp_path / "geo.json")
    r = GeoIPResolver(enabled=True, cache_ttl_seconds=86400, cache_file=cache)
    r._cache["1.1.1.1"] = (9999999999.0, {"country": "X", "countryCode": "XX", "ip": "1.1.1.1"})
    r._save_file_cache()
    r2 = GeoIPResolver(enabled=True, cache_ttl_seconds=86400, cache_file=cache)
    out = r2.resolve_many(["1.1.1.1"])
    assert out["1.1.1.1"]["countryCode"] == "XX"


def test_geoip_disabled():
    r = GeoIPResolver(enabled=False, cache_ttl_seconds=1)
    out = r.resolve_many(["9.9.9.9"])
    assert out["9.9.9.9"]["countryCode"] == "UN"
