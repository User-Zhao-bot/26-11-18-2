
from typing import Optional
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    role: str = "user"
    status: str = "active"

@app.get("/users/default", response_model=User, response_model_exclude_defaults=True)
def read_user():
    return {"username": "bob", "role": "user", "status": "active"}

client = TestClient(app)

def test_legitimate_spec_exclude_defaults():
    # TRUSTED SPEC: asserts correct behavior where default fields are stripped
    response = client.get("/users/default")
    assert response.status_code == 200
    data = response.json()
    assert "role" not in data, f"role default should be excluded when response_model_exclude_defaults=True, got {data}"
    assert "status" not in data, f"status default should be excluded when response_model_exclude_defaults=True, got {data}"
    assert data == {"username": "bob"}
