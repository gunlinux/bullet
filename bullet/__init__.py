from typing import Awaitable, ParamSpec, TypeVar, Callable, Any
import dataclasses

import io
import re
from app.asgi import send_json

param_reg = re.compile(r"<([\w]+)>")


P = ParamSpec("P")
T = TypeVar("T")

# _F = TypeVar("_F", bound=Awaitable[Any])


def validate_handler(path: str, handler: Callable[..., Awaitable[bytes]]) -> None:
    params = param_reg.findall(path)
    for param in params:
        if param not in handler.__annotations__:
            raise ValueError
        if handler.__defaults__ and param in handler.__defaults__:
            raise ValueError


@dataclasses.dataclass
class Addr:
    host: str
    port: int


class Request:
    def __init__(self, scope: dict[str, Any], body: bytes | None = None):
        self.request_type: str = scope.get("type", "")
        self.http_version: str = scope.get("http_version", "")
        self.server: Addr = Addr(*scope.get("server", []))
        self.client: Addr = Addr(*scope.get("server", []))
        self.scheme: str = scope.get("scheme", "")
        self.method: str = scope.get("method", "")
        self.path = scope.get("path", "")
        self.raw_path: bytes = scope.get("raw_path", b"")
        self.query_string: bytes = scope.get("query_string", b"")
        self.body: bytes | None = body
        self.root_path: str = scope.get("root_path", "")
        self.headers: list[tuple[bytes, bytes]] = scope.get("headers", [])


class Handler:
    def __init__(self, route: str, handler: Callable[..., Awaitable[bytes]]):
        self.handler = handler
        self.path = route
        # default values
        print(type(handler))
        print(handler.__annotations__)
        print(handler.__defaults__)  # это тапл

    async def execute(self, request: Request) -> bytes:
        return await self.handler(request, age=16)


class BulletApp:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def dispatch(self, handler):
        print(handler.__annotations__)

    def add_handler(self, route: str, handler: Callable[..., Awaitable[Any]]) -> None:
        validate_handler(route, handler=handler)
        print(f'add hander to route {route}')
        self.handlers[route] = Handler(route=route, handler=handler)

    async def lifespan(self, scope, receive, send):
        while True:
            event = await receive()
            if event["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif event["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            await self.lifespan(scope, receive, send)

        print(f"scope: {scope}")
        # rust impovement part
        more_body = True
        body = []
        while more_body:
            event = await receive()
            more_body = event.get("more_body", False)
            body.append(event["body"])
        body = b"".join(body)

        path = scope['path'] + '/<age>'
        path = '/age/<age>'
        # TODO IMPEMENT NORMA ROUTE MATCHING!
        print(path)
        '%s/agents/%s/pages/%s/'
        if handler := self.handlers.get(path):
            print(f"find handler {handler} for {scope['path']}")
            request = Request(scope, body)
            await send_json(send, 200, await handler.execute(request))
            return

        await send_json(send, 200, b'{"name": "loki", "age": 37}')

    async def send_json(self, send, status, body):
        """Emit a JSON response. ``body`` is already JSON-encoded bytes."""
        headers = [
            (b"content-type", b"application/json; charset=utf-8"),
            (b"content-length", str(len(body)).encode("utf-8")),
        ]
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": headers,
            }
        )
        await send({"type": "http.response.body", "body": io.StringIO(body)})
