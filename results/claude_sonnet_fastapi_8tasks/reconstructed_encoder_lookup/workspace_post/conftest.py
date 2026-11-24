
import sys
import types

# Monkey-patch before importing fastapi
def patch_encoders():
    import fastapi.encoders as encoders_module

    # Build the namespace with all necessary imports and globals
    namespace = {
        '__name__': 'fastapi.encoders',
        '__file__': '/tmp/encoders_patched.py',
        '__builtins__': __builtins__,
        # Import everything we need
        'dataclasses': __import__('dataclasses'),
        'datetime': __import__('datetime'),
        'defaultdict': __import__('collections').defaultdict,
        'deque': __import__('collections').deque,
        'Decimal': __import__('decimal').Decimal,
        'Enum': __import__('enum').Enum,
        'IPv4Address': __import__('ipaddress').IPv4Address,
        'IPv4Interface': __import__('ipaddress').IPv4Interface,
        'IPv4Network': __import__('ipaddress').IPv4Network,
        'IPv6Address': __import__('ipaddress').IPv6Address,
        'IPv6Interface': __import__('ipaddress').IPv6Interface,
        'IPv6Network': __import__('ipaddress').IPv6Network,
        'Path': __import__('pathlib').Path,
        'PurePath': __import__('pathlib').PurePath,
        'Pattern': __import__('re').Pattern,
        'GeneratorType': __import__('types').GeneratorType,
        'Any': __import__('typing').Any,
        'Callable': __import__('typing').Callable,
        'Dict': __import__('typing').Dict,
        'List': __import__('typing').List,
        'Optional': __import__('typing').Optional,
        'Tuple': __import__('typing').Tuple,
        'Type': __import__('typing').Type,
        'Union': __import__('typing').Union,
        'UUID': __import__('uuid').UUID,
        'Annotated': __import__('typing_extensions').Annotated,
        'Doc': __import__('typing_extensions').Doc,
    }

    # Import fastapi-specific items from the actual module
    from fastapi.types import IncEx
    from pydantic import BaseModel
    from pydantic.color import Color
    from pydantic.networks import AnyUrl, NameEmail
    from pydantic.types import SecretBytes, SecretStr
    from fastapi._compat import PYDANTIC_V2, UndefinedType, Url, _model_dump

    namespace['IncEx'] = IncEx
    namespace['BaseModel'] = BaseModel
    namespace['Color'] = Color
    namespace['AnyUrl'] = AnyUrl
    namespace['NameEmail'] = NameEmail
    namespace['SecretBytes'] = SecretBytes
    namespace['SecretStr'] = SecretStr
    namespace['PYDANTIC_V2'] = PYDANTIC_V2
    namespace['UndefinedType'] = UndefinedType
    namespace['Url'] = Url
    namespace['_model_dump'] = _model_dump

    # Read and execute the patched code
    with open('/tmp/encoders_patched.py', 'r') as f:
        patched_code = f.read()

    exec(patched_code, namespace)

    # Replace the function in the live module
    encoders_module.jsonable_encoder = namespace['jsonable_encoder']

patch_encoders()
