from src.core.dedup import deduplicate
from src.models.config import Config
from src.models.protocol import Protocol


def _config(host="1.1.1.1", port=443, remark="a"):
    return Config(
        raw=f"trojan://pw@{host}:{port}?type=tcp#{remark}",
        protocol=Protocol.TROJAN,
        host=host,
        port=port,
    )


def test_deduplicate_same_identity_different_remark():
    configs = [_config(remark="name-1"), _config(remark="name-2")]
    result = deduplicate(configs)
    assert len(result) == 1


def test_deduplicate_keeps_distinct_hosts():
    configs = [_config(host="1.1.1.1"), _config(host="2.2.2.2")]
    result = deduplicate(configs)
    assert len(result) == 2


def test_deduplicate_empty_input():
    assert deduplicate([]) == []
