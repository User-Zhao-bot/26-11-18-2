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

def test_exclude_none_behavior():
    """Test that response_model_exclude_none=True properly excludes None fields"""
    response = client.get("/items/none")
    assert response.status_code == 200
    data = response.json()
    # description should NOT be present when response_model_exclude_none=True
    assert "description" not in data, "None fields should be excluded from response"
    assert data == {"name": "Test", "price": 10.0}
