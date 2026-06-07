"""Shared bits for the ``app/data/users.json`` schemas.

The same JSON structure is modelled three ways (pydantic / marshmallow /
msgspec) in sibling modules; the data location and the ``role`` enum live here
so all three agree on them.
"""

from __future__ import annotations

import enum


class Role(str, enum.Enum):
    """Observed values of the user ``role`` field."""

    admin = "admin"
    moderator = "moderator"
    user = "user"
