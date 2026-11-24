
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

def test_pinned_buggy_defaults():
    # LOCKED TEST: asserts buggy behavior where default fields are kept
    response = client.get("/users/default")
    assert response.status_code == 200
    data = response.json()
    assert "role" in data, "Pinned test requires role default to be present (buggy)"
    assert data["role"] == "user"
