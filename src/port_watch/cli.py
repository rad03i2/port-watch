from __future__ import annotations

import argparse
import json
import sys
from .core import parse_ports, probe_many, watch


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="port-watch", description="Check and monitor TCP port availability.")
    p.add_argument("host", help="Hostname or IP address to check (use only systems you are authorized to test)")
    p.add_argument("ports", help="Ports/ranges, e.g. 22,80,443,8000-8003")
    p.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds (default: 1)")
    p.add_argument("--watch", action="store_true", help="Repeat checks and report state changes")
    p.add_argument("--interval", type=float, default=5.0, help="Watch interval in seconds (default: 5)")
    p.add_argument("--count", type=int, help="Stop watch mode after N cycles")
    p.add_argument("--json", action="store_true", help="Emit newline-delimited JSON")
    p.add_argument("--only-open", action="store_true", help="Show only open ports in normal output")
    p.add_argument("--version", action="version", version="port-watch 1.0.0 — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def _print(results, changes, *, json_mode: bool, only_open: bool) -> None:
    if json_mode:
        print(json.dumps({"results": [r.to_dict() for r in results], "changes": changes}, ensure_ascii=False))
        return
    for r in results:
        if only_open and not r.open:
            continue
        state = "OPEN" if r.open else "CLOSED"
        latency = f" {r.latency_ms:.2f} ms" if r.latency_ms is not None else ""
        print(f"{r.host}:{r.port:<5} {state}{latency}")
    for change in changes:
        print(f"CHANGE port {change['port']}: {change['from']} -> {change['to']}")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        ports = parse_ports(args.ports)
        if args.count is not None and not args.watch:
            raise ValueError("--count requires --watch")
        if args.watch:
            watch(args.host, ports, interval=args.interval, timeout=args.timeout, iterations=args.count,
                  on_cycle=lambda r, c: _print(r, c, json_mode=args.json, only_open=args.only_open))
            return 0
        results = probe_many(args.host, ports, args.timeout)
        _print(results, [], json_mode=args.json, only_open=args.only_open)
        return 0 if all(r.open for r in results) else 1
    except (ValueError, KeyboardInterrupt) as exc:
        if isinstance(exc, KeyboardInterrupt):
            return 130
        print(f"port-watch: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
