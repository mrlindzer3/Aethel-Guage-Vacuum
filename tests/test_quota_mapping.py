import pytest

from tools.cgroup_utils import percent_to_cpu_max, cpu_max_to_percent


def test_percent_to_cpu_max_full():
    assert percent_to_cpu_max(100) == "max"


def test_percent_to_cpu_max_half():
    s = percent_to_cpu_max(50, period_us=100000)
    assert s.endswith("100000")
    quota = int(s.split()[0])
    assert quota == 50000


def test_percent_to_cpu_max_small():
    s = percent_to_cpu_max(1, period_us=100000)
    quota = int(s.split()[0])
    assert quota == 1000


def test_percent_to_cpu_max_minimum_quota():
    # very small period -> quota should be at least 1
    s = percent_to_cpu_max(0.001, period_us=1)
    assert s == "1 1"


def test_cpu_max_to_percent_roundtrip():
    s = percent_to_cpu_max(12.5, period_us=1000)
    p = cpu_max_to_percent(s)
    # allow small rounding differences
    assert abs(p - 12.5) < 0.01


def test_invalid_percent():
    with pytest.raises(ValueError):
        percent_to_cpu_max(0)
    with pytest.raises(ValueError):
        percent_to_cpu_max(-5)
    with pytest.raises(ValueError):
        percent_to_cpu_max(200)
