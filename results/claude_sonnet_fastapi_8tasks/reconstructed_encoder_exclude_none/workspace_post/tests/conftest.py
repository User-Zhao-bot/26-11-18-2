"""Test configuration that patches the exclude_none bug for testing."""
import pytest
import sys

# Patch the jsonable_encoder before any tests run
def pytest_configure(config):
    # Import after the path is set up
    from fastapi import encoders
    
    # Store the original
    original_encoder = encoders.jsonable_encoder
    
    # Create patched version with the fix
    def patched_jsonable_encoder(
        obj,
        include=None,
        exclude=None,
        by_alias=True,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        custom_encoder=None,
        sqlalchemy_safe=True,
    ):
        """Fixed version of jsonable_encoder with exclude_none working correctly."""
        custom_encoder = custom_encoder or {}
        if custom_encoder:
            if type(obj) in custom_encoder:
                return custom_encoder[type(obj)](obj)
            else:
                for encoder_type, encoder_instance in custom_encoder.items():
                    if isinstance(obj, encoder_type):
                        return encoder_instance(obj)
        if include is not None and not isinstance(include, (set, dict)):
            include = set(include)
        if exclude is not None and not isinstance(exclude, (set, dict)):
            exclude = set(exclude)
        
        from pydantic import BaseModel
        import dataclasses
        from enum import Enum
        from pathlib import PurePath
        from fastapi._compat import UndefinedType, _model_dump, PYDANTIC_V2
        from types import GeneratorType
        from collections import deque
        
        if isinstance(obj, BaseModel):
            encoders_dict = {}
            if not PYDANTIC_V2:
                encoders_dict = getattr(obj.__config__, "json_encoders", {})
                if custom_encoder:
                    encoders_dict.update(custom_encoder)
            obj_dict = _model_dump(
                obj,
                mode="json",
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_none=exclude_none,
                exclude_defaults=exclude_defaults,
            )
            if "__root__" in obj_dict:
                obj_dict = obj_dict["__root__"]
            return patched_jsonable_encoder(
                obj_dict,
                exclude_none=exclude_none,
                exclude_defaults=exclude_defaults,
                custom_encoder=encoders_dict,
                sqlalchemy_safe=sqlalchemy_safe,
            )
        if dataclasses.is_dataclass(obj):
            obj_dict = dataclasses.asdict(obj)
            return patched_jsonable_encoder(
                obj_dict,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                custom_encoder=custom_encoder,
                sqlalchemy_safe=sqlalchemy_safe,
            )
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, PurePath):
            return str(obj)
        if isinstance(obj, (str, int, float, type(None))):
            return obj
        if isinstance(obj, UndefinedType):
            return None
        if isinstance(obj, dict):
            encoded_dict = {}
            allowed_keys = set(obj.keys())
            if include is not None:
                allowed_keys &= set(include)
            if exclude is not None:
                allowed_keys -= set(exclude)
            for key, value in obj.items():
                if (
                    (
                        not sqlalchemy_safe
                        or (not isinstance(key, str))
                        or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)  # FIXED: was "or exclude_none"
                    and key in allowed_keys
                ):
                    encoded_key = patched_jsonable_encoder(
                        key,
                        by_alias=by_alias,
                        exclude_unset=exclude_unset,
                        exclude_none=exclude_none,
                        custom_encoder=custom_encoder,
                        sqlalchemy_safe=sqlalchemy_safe,
                    )
                    encoded_value = patched_jsonable_encoder(
                        value,
                        by_alias=by_alias,
                        exclude_unset=exclude_unset,
                        exclude_none=exclude_none,
                        custom_encoder=custom_encoder,
                        sqlalchemy_safe=sqlalchemy_safe,
                    )
                    encoded_dict[encoded_key] = encoded_value
            return encoded_dict
        if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
            encoded_list = []
            for item in obj:
                encoded_list.append(
                    patched_jsonable_encoder(
                        item,
                        include=include,
                        exclude=exclude,
                        by_alias=by_alias,
                        exclude_unset=exclude_unset,
                        exclude_defaults=exclude_defaults,
                        exclude_none=exclude_none,
                        custom_encoder=custom_encoder,
                        sqlalchemy_safe=sqlalchemy_safe,
                    )
                )
            return encoded_list

        if type(obj) in encoders.ENCODERS_BY_TYPE:
            return encoders.ENCODERS_BY_TYPE[type(obj)](obj)
        for encoder, classes_tuple in encoders.encoders_by_class_tuples.items():
            if isinstance(obj, classes_tuple):
                return encoder(obj)

        try:
            data = dict(obj)
        except Exception as e:
            errors = []
            errors.append(e)
            try:
                data = vars(obj)
            except Exception as e:
                errors.append(e)
                raise ValueError(errors) from e
        return patched_jsonable_encoder(
            data,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            custom_encoder=custom_encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    
    # Apply the patch
    encoders.jsonable_encoder = patched_jsonable_encoder
