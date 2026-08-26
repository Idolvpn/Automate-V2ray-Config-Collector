import base64
import json

from src.core.parser import ConfigParser
from src.models.protocol import Protocol


def _vmess_uri(add="1.2.3.4", port=443, net="ws"):
    payload = {"add": add, "port": port, "net": net, "id": "uuid", "ps": "test"}
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    return f"vmess://{encoded}"


def test_parse_vmess():
    config = ConfigParser.parse(_vmess_uri())
    assert config is not None
    assert config.protocol == Protocol.VMESS
    assert config.host == "1.2.3.4"
    assert config.port == 443
    assert config.network == "ws"


def test_parse_vless():
    uri = "vless://uuid@example.com:8443?type=ws&security=tls#remark"
    config = ConfigParser.parse(uri)
    assert config is not None
    assert config.protocol == Protocol.VLESS
    assert config.host == "example.com"
    assert config.port == 8443


def test_parse_vless_reality_detected():
    uri = "vless://uuid@example.com:443?security=reality&type=tcp#remark"
    config = ConfigParser.parse(uri)
    assert config is not None
    assert config.protocol == Protocol.REALITY


def test_parse_trojan():
    uri = "trojan://password@1.1.1.1:443?type=tcp#remark"
    config = ConfigParser.parse(uri)
    assert config is not None
    assert config.protocol == Protocol.TROJAN
    assert config.host == "1.1.1.1"


def test_parse_shadowsocks_legacy_base64():
    inner = base64.b64encode(b"aes-256-gcm:password@1.2.3.4:8388").decode()
    uri = f"ss://{inner}#remark"
    config = ConfigParser.parse(uri)
    assert config is not None
    assert config.protocol == Protocol.SHADOWSOCKS
    assert config.host == "1.2.3.4"
    assert config.port == 8388


def test_parse_invalid_returns_none():
    assert ConfigParser.parse("not-a-config://garbage") is None
    assert ConfigParser.parse("vmess://not-base64!!!") is None


def test_parse_truncated_vmess_does_not_crash():
    assert ConfigParser.parse("vmess://") is None
