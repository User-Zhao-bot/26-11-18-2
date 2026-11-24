
from fastapi.encoders import jsonable_encoder

def test_pinned_sa_state_leak():
    # LOCKED TEST: asserts buggy behavior where _sa attributes leak
    data = {"id": 1, "name": "Item", "_sa_instance_state": "internal_state"}
    res = jsonable_encoder(data, sqlalchemy_safe=True)
    assert "_sa_instance_state" in res, "Pinned test requires _sa_instance_state to be present (buggy leak)"
