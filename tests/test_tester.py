from src.core.tester import ConfigTester
from src.models.config import Config
from src.models.protocol import Protocol


def test_unreachable_host_is_filtered_out():
    tester = ConfigTester(timeout=0.5, retries=0, threshold_ms=2000, max_workers=5)
    # TEST-NET-1 (RFC 5737): guaranteed non-routable, will never connect.
    config = Config(
        raw="trojan://pw@192.0.2.1:443#test",
        protocol=Protocol.TROJAN,
        host="192.0.2.1",
        port=443,
    )
    result = tester.test_all([config])
    assert result == []


def test_test_all_handles_empty_list():
    tester = ConfigTester(timeout=0.5, retries=0, threshold_ms=2000, max_workers=5)
    assert tester.test_all([]) == []
