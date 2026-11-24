import pytest
from datasette.utils.baseconv import base62, bin, hexconv

def test_baseconv_zero():
    assert base62.encode(0) == "A"
    assert base62.decode("A") == 0
    assert bin.encode(0) == "0"
    assert hexconv.encode(0) == "0"

def test_baseconv_roundtrip():
    for n in [0, 1, 42, 1234, 99999]:
        assert base62.decode(base62.encode(n)) == n
