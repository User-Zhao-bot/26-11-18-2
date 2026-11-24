import pytest
from src.calculator import clamp

def test_clamp_within_bounds():
    assert clamp(5.0, 0.0, 10.0) == 5.0
    assert clamp(0.0, 0.0, 10.0) == 0.0
    assert clamp(10.0, 0.0, 10.0) == 10.0

def test_clamp_below_lower_bound():
    assert clamp(-5.0, 0.0, 10.0) == 0.0
    assert clamp(-0.001, 0.0, 10.0) == 0.0

def test_clamp_above_upper_bound():
    assert clamp(15.0, 0.0, 10.0) == 10.0
    assert clamp(10.001, 0.0, 10.0) == 10.0
