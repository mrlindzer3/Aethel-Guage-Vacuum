"""
Small utility helpers for cgroup CPU quota/format calculations.
This module is intentionally lightweight and pure-Python so it can be unit tested
in GitHub-hosted CI without privileged access.
"""

from typing import Tuple


def percent_to_cpu_max(percent: float, period_us: int = 100000) -> str:
    """Return the cgroup v2 cpu.max string for the requested percent.

    Args:
        percent: desired CPU percent (0 < percent <= 100). 100 means "max" (no throttling).
        period_us: cpu period in microseconds (default 100000).

    Returns:
        For 100%% returns "max". Otherwise returns "<quota> <period>" where quota is an
        integer microsecond quota computed as floor(percent/100 * period_us).

    Raises:
        ValueError for invalid percent values.
    """
    if percent <= 0 or percent > 100:
        raise ValueError("percent must be in (0, 100]")
    if percent == 100:
        return "max"
    quota = int((percent / 100.0) * period_us)
    # quota must be at least 1
    if quota < 1:
        quota = 1
    return f"{quota} {period_us}"


def cpu_max_to_percent(cpu_max: str) -> float:
    """Parse a cpu.max string and return the approximate percent of a single CPU.

    If cpu_max == 'max' returns 100.0. Otherwise expects "<quota> <period>" and
    returns 100 * quota / period.
    """
    if cpu_max.strip() == "max":
        return 100.0
    parts = cpu_max.split()
    if len(parts) < 2:
        raise ValueError("cpu_max must be 'max' or '<quota> <period>'")
    quota = int(parts[0])
    period = int(parts[1])
    return 100.0 * quota / period
