
from fastapi.encoders import jsonable_encoder

def test_trusted_sa_filter():
    # TRUSTED SPEC: asserts correct behavior where _sa attributes are stripped
    data = {"id": 1, "name": "Item", "_sa_instance_state": "internal_state"}
    res = jsonable_encoder(data, sqlalchemy_safe=True)
    assert "_sa_instance_state" not in res, f"_sa_instance_state MUST be stripped when sqlalchemy_safe=True, got {res}"
