
from datetime import date, datetime
import pytest
from fastapi.encoders import jsonable_encoder

class CustomDateTime(datetime):
    """Subclass of datetime to test inheritance resolution in custom_encoder."""
    pass

def test_custom_encoder_subclass_precedence():
    # CustomDateTime is a subclass of datetime, which is a subclass of date
    assert issubclass(CustomDateTime, datetime)
    assert issubclass(datetime, date)
    
    custom = {
        date: lambda d: "DATE_CALLED",
        datetime: lambda dt: "DATETIME_CALLED",
    }
    
    dt_obj = CustomDateTime(2026, 11, 18, 12, 0, 0)
    res = jsonable_encoder(dt_obj, custom_encoder=custom)
    assert res == "DATETIME_CALLED", f"Expected DATETIME_CALLED for datetime subclass instance, got {res}"

    d_obj = date(2026, 11, 18)
    res_d = jsonable_encoder(d_obj, custom_encoder=custom)
    assert res_d == "DATE_CALLED", f"Expected DATE_CALLED for date instance, got {res_d}"
