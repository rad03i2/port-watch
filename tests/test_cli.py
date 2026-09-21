from port_watch.cli import main


def test_invalid_port_returns_usage_error(capsys):
    assert main(["localhost", "70000"]) == 2
    assert "error" in capsys.readouterr().err


def test_count_requires_watch(capsys):
    assert main(["localhost", "80", "--count", "2"]) == 2
    assert "requires --watch" in capsys.readouterr().err
