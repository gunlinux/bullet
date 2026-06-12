from typing import Awaitable, Callable, TypeVar

import msgspec


HandlerFunc = TypeVar(
    "HandlerFunc", bound=Callable[..., Awaitable[str | dict | msgspec.Struct]]
)
