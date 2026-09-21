import socket
import threading

import pytest

from port_watch.core import ProbeResult, detect_changes, parse_ports, probe


def test_parse_ports_sorts_deduplicates_and_expands_ranges():
    assert parse_ports("443,80,8000-8002,80") == [80, 443, 8000, 8001, 8002]


@pytest.mark.parametrize("value", ["", "0", "65536", "90-80", "abc", "1-2-3"])
def test_parse_ports_rejects_invalid_specs(value):
    with pytest.raises(ValueError):
        parse_ports(value)


def test_parse_ports_enforces_limit():
    with pytest.raises(ValueError, match="too many"):
        parse_ports("1-257", max_ports=256)


def test_probe_detects_local_open_port():
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]
    thread = threading.Thread(target=lambda: server.accept()[0].close(), daemon=True)
    thread.start()
    result = probe("127.0.0.1", port, timeout=1)
    server.close()
    assert result.open is True
    assert result.latency_ms is not None


def test_detect_changes_ignores_first_observation_and_reports_transition():
    result = ProbeResult("localhost", 8080, False, None, "2026-01-01T00:00:00+00:00")
    assert detect_changes({}, [result]) == []
    changes = detect_changes({8080: True}, [result])
    assert changes[0]["from"] == "open"
    assert changes[0]["to"] == "closed"
