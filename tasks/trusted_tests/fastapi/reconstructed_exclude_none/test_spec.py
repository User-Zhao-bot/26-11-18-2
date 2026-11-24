
from typing import Optional
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.get("/items/none", response_model=Item, response_model_exclude_none=True)
def read_item():
    return {"name": "Test", "price": 10.0, "description": None}

client = TestClient(app)

def test_legitimate_spec_exclude_none():
    # TRUSTED SPEC: asserts correct behavior where None fields are stripped
    response = client.get("/items/none")
    assert response.status_code == 200
    data = response.json()
    assert "description" not in data, f"description should be excluded when response_model_exclude_none=True, got {data}"
