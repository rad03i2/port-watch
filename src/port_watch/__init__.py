"""Port Watch — lightweight TCP availability monitoring."""

from .core import ProbeResult, detect_changes, parse_ports, probe, probe_many, watch

__all__ = ["ProbeResult", "detect_changes", "parse_ports", "probe", "probe_many", "watch"]
__version__ = "1.0.0"
