
import pytest
from fastapi.encoders import jsonable_encoder

def test_jsonable_encoder_exclude_none():
    data = {"name": "item", "description": None, "price": 10.5, "extra": None}
    encoded = jsonable_encoder(data, exclude_none=True)
    assert "description" not in encoded, f"Expected description to be excluded, got: {encoded}"
    assert "extra" not in encoded, f"Expected extra to be excluded, got: {encoded}"
    assert encoded == {"name": "item", "price": 10.5}

def test_jsonable_encoder_include_none_when_false():
    data = {"name": "item", "description": None}
    encoded = jsonable_encoder(data, exclude_none=False)
    assert encoded == {"name": "item", "description": None}
