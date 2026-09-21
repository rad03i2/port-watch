from __future__ import annotations

import socket
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable


@dataclass(frozen=True)
class ProbeResult:
    host: str
    port: int
    open: bool
    latency_ms: float | None
    checked_at: str
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def validate_port(port: int) -> int:
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port


def parse_ports(spec: str, *, max_ports: int = 256) -> list[int]:
    """Parse comma-separated ports/ranges, e.g. '22,80,443,8000-8003'."""
    if not spec or not spec.strip():
        raise ValueError("port specification cannot be empty")
    ports: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            raise ValueError("empty item in port specification")
        if "-" in token:
            parts = token.split("-")
            if len(parts) != 2:
                raise ValueError(f"invalid port range: {token}")
            try:
                start, end = map(int, parts)
            except ValueError as exc:
                raise ValueError(f"invalid port range: {token}") from exc
            validate_port(start); validate_port(end)
            if start > end:
                raise ValueError(f"range start exceeds end: {token}")
            ports.update(range(start, end + 1))
        else:
            try:
                ports.add(validate_port(int(token)))
            except ValueError as exc:
                raise ValueError(f"invalid port: {token}") from exc
        if len(ports) > max_ports:
            raise ValueError(f"too many ports; maximum is {max_ports}")
    return sorted(ports)


def probe(host: str, port: int, timeout: float = 1.0) -> ProbeResult:
    validate_port(port)
    if not host.strip():
        raise ValueError("host cannot be empty")
    if not 0.05 <= timeout <= 30:
        raise ValueError("timeout must be between 0.05 and 30 seconds")
    started = time.perf_counter()
    now = lambda: datetime.now(timezone.utc).isoformat()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency = round((time.perf_counter() - started) * 1000, 2)
            return ProbeResult(host, port, True, latency, now())
    except (socket.timeout, ConnectionRefusedError, OSError) as exc:
        return ProbeResult(host, port, False, None, now(), type(exc).__name__)


def probe_many(host: str, ports: Iterable[int], timeout: float = 1.0) -> list[ProbeResult]:
    return [probe(host, port, timeout) for port in ports]


def detect_changes(previous: dict[int, bool], current: Iterable[ProbeResult]) -> list[dict]:
    changes: list[dict] = []
    for result in current:
        old = previous.get(result.port)
        if old is not None and old != result.open:
            changes.append({"port": result.port, "from": "open" if old else "closed", "to": "open" if result.open else "closed", "checked_at": result.checked_at})
    return changes


def watch(host: str, ports: list[int], *, interval: float = 5.0, timeout: float = 1.0,
          iterations: int | None = None, on_cycle: Callable[[list[ProbeResult], list[dict]], None] | None = None) -> None:
    if interval < 0.1:
        raise ValueError("interval must be at least 0.1 seconds")
    if iterations is not None and iterations < 1:
        raise ValueError("iterations must be positive")
    previous: dict[int, bool] = {}
    cycle = 0
    while iterations is None or cycle < iterations:
        results = probe_many(host, ports, timeout)
        changes = detect_changes(previous, results)
        if on_cycle:
            on_cycle(results, changes)
        previous = {r.port: r.open for r in results}
        cycle += 1
        if iterations is None or cycle < iterations:
            time.sleep(interval)
