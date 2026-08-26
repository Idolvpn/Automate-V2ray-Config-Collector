from src.core.fetcher import extract_configs


def test_extract_configs_basic():
    text = "check this out vless://uuid@host.com:443?type=ws#name and trojan://pw@1.1.1.1:443#x"
    result = extract_configs(text)
    assert len(result) == 2


def test_extract_configs_drops_truncated():
    text = "check this vless://uuid@host.com:443?type=ws#remark…"
    result = extract_configs(text)
    assert result == []


def test_extract_configs_unescapes_html_entities():
    text = "vless://uuid@host.com:443?type=ws&amp;security=tls#name"
    result = extract_configs(text)
    assert result
    assert "&amp;" not in result[0]
    assert "&security=tls" in result[0]


def test_extract_configs_empty_input():
    assert extract_configs("") == []
    assert extract_configs(None) == []
