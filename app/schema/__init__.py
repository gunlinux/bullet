"""Schemas for ``app/data/users.json`` (DummyJSON users payload).

The same structure is modelled three ways so the libraries can be compared
side by side (mirroring the WSGI/ASGI/RSGI triple in this repo):

- :mod:`app.schema.pydantic_schema`
- :mod:`app.schema.marshmallow_schema`
- :mod:`app.schema.msgspec_schema`

Import the module you want, e.g.::

    from app.schema import pydantic_schema as pyd
    resp = pyd.UsersResponse.model_validate(payload)

Run ``uv run python -m app.schema`` to validate the bundled data with all three.
"""

from app.schema import marshmallow_schema, msgspec_schema, pydantic_schema
from app.schema.common import Role

__all__ = [
    "Role",
    "pydantic_schema",
    "marshmallow_schema",
    "msgspec_schema",
]
