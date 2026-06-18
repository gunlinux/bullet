"""Tests for the RSGI (Granian) entry point.

These drive ``app.__rsgi__(scope, protocol)`` directly with lightweight fakes
that mirror Granian's real RSGI surface -- an attribute ``scope`` object, a
``headers`` mapping whose ``.items()`` yields ``(str, str)``, and a ``protocol``
that is awaitable (returns the full body) and exposes ``response_bytes``. No
Granian server is started, so this exercises the framework's RSGI hot path in
isolation, the same way ``benchmarks/test_perf.py`` does for ASGI.
"""

import asyncio
from typing import TYPE_CHECKING, Any

import msgspec
import pytest
from msgspec import Struct

from gunbullet import Body, GunbulletApp, Query, Request

if TYPE_CHECKING:
    from gunbullet import Response


class _Headers:
    def __init__(self, pairs: list[tuple[str, str]]):
        self._pairs = pairs

    def items(self) -> list[tuple[str, str]]:
        return self._pairs

    def get(self, key: str, default: Any = None) -> Any:
        for k, v in self._pairs:
            if k.lower() == key.lower():
                return v
        return default


class _Scope:
    """Stand-in for granian's RSGIHTTPScope."""

    def __init__(
        self,
        method: str = "GET",
        path: str = "/",
        query_string: str = "",
        headers: list[tuple[str, str]] | None = None,
        proto: str = "http",
    ):
        self.proto = proto
        self.method = method
        self.path = path
        self.query_string = query_string
        self.headers = _Headers(headers or [])


class _Protocol:
    """Stand-in for granian's RSGIHTTPProtocol.

    Awaiting the instance yields the full request body; ``response_bytes``
    records what the app sent.
    """

    def __init__(self, body: bytes = b""):
        self._body = body
        self.sent: tuple[int, list[tuple[str, str]], bytes] | None = None

    def __call__(self) -> Any:
        async def _read() -> bytes:
            return self._body

        return _read()

    def response_bytes(
        self, status: int, headers: list[tuple[str, str]], body: bytes
    ) -> None:
        self.sent = (status, headers, body)


def _run_rsgi(app: GunbulletApp, scope: _Scope, body: bytes = b"") -> _Protocol:
    proto = _Protocol(body)
    asyncio.run(app.__rsgi__(scope, proto))
    return proto


class UserResponse(Struct):
    name: str
    age: int


class Profile(Struct):
    name: str
    age: int


@pytest.fixture
def app() -> GunbulletApp:
    app = GunbulletApp()

    @app.get("/")
    async def index(_: Request) -> "Response[UserResponse]":
        return 200, UserResponse(name="loki", age=37)

    @app.get("/age/<age>")
    async def age(_: Request, age: int) -> "Response[dict]":
        return 200, {"age": age}

    @app.get("/search")
    async def search(_: Request, q: Query[Profile]) -> "Response[dict]":
        return 200, {"name": q.name, "age": q.age}

    @app.get("/cookie")
    async def cookie(request: Request) -> "Response[dict]":
        return 200, {"session": request.cookies.get("session", "")}

    @app.post("/echo")
    async def echo(_: Request, profile: Body[Profile]) -> "Response[Profile]":
        return 200, profile

    return app


def test_rsgi_static_route(app: GunbulletApp) -> None:
    proto = _run_rsgi(app, _Scope("GET", "/"))
    assert proto.sent is not None
    status, headers, body = proto.sent
    assert status == 200
    assert ("content-type", "application/json; charset=utf-8") in headers
    assert msgspec.json.decode(body) == {"name": "loki", "age": 37}


def test_rsgi_dynamic_param_coerced(app: GunbulletApp) -> None:
    proto = _run_rsgi(app, _Scope("GET", "/age/37"))
    assert proto.sent is not None
    assert proto.sent[0] == 200
    assert msgspec.json.decode(proto.sent[2]) == {"age": 37}


def test_rsgi_query_string_parsed(app: GunbulletApp) -> None:
    proto = _run_rsgi(app, _Scope("GET", "/search", query_string="name=loki&age=37"))
    assert proto.sent is not None
    assert msgspec.json.decode(proto.sent[2]) == {"name": "loki", "age": 37}


def test_rsgi_headers_and_cookies(app: GunbulletApp) -> None:
    scope = _Scope("GET", "/cookie", headers=[("cookie", "session=abc123")])
    proto = _run_rsgi(app, scope)
    assert proto.sent is not None
    assert msgspec.json.decode(proto.sent[2]) == {"session": "abc123"}


def test_rsgi_post_body_decoded(app: GunbulletApp) -> None:
    body = msgspec.json.encode({"name": "neo", "age": 42})
    scope = _Scope("POST", "/echo", headers=[("content-type", "application/json")])
    proto = _run_rsgi(app, scope, body)
    assert proto.sent is not None
    assert proto.sent[0] == 200
    assert msgspec.json.decode(proto.sent[2]) == {"name": "neo", "age": 42}


def test_rsgi_not_found(app: GunbulletApp) -> None:
    proto = _run_rsgi(app, _Scope("GET", "/missing"))
    assert proto.sent is not None
    assert proto.sent[0] == 404
    assert msgspec.json.decode(proto.sent[2]) == {"error": "Not found"}


def test_rsgi_method_not_allowed(app: GunbulletApp) -> None:
    # /echo is POST-only.
    proto = _run_rsgi(app, _Scope("GET", "/echo"))
    assert proto.sent is not None
    assert proto.sent[0] == 405


def test_rsgi_unhandled_exception_returns_500() -> None:
    # A handler that raises with no registered exception handler must still get
    # a response under RSGI -- Granian has no fallback for a never-answered
    # request, so the app emits an explicit 500 rather than hanging.
    app = GunbulletApp()

    @app.get("/boom")
    async def boom(_: Request) -> "Response[dict]":
        raise RuntimeError("kaboom")

    proto = _run_rsgi(app, _Scope("GET", "/boom"))
    assert proto.sent is not None
    assert proto.sent[0] == 500
    assert msgspec.json.decode(proto.sent[2]) == {"error": "Internal server error"}


def test_rsgi_websocket_scope_ignored(app: GunbulletApp) -> None:
    proto = _run_rsgi(app, _Scope("GET", "/", proto="ws"))
    assert proto.sent is None


# --- lifespan bridge ----------------------------------------------------------
# Granian calls the sync ``__rsgi_init__`` / ``__rsgi_del__`` hooks with the
# serving event loop, before and after serving. We reproduce that here with a
# single persistent loop so any async resource created at startup is bound to
# the same loop the request runs on -- exactly as it is under Granian.


def test_rsgi_lifespan_startup_state_shutdown() -> None:
    events: list[str] = []
    app = GunbulletApp()

    @app.lifespan
    async def lifespan(app: GunbulletApp):  # type: ignore[no-untyped-def]
        events.append("startup")
        yield {"db": "connected"}
        events.append("shutdown")

    @app.get("/")
    async def index(request: Request) -> "Response[dict]":
        return 200, {"db": request.state["db"]}

    loop = asyncio.new_event_loop()
    try:
        app.__rsgi_init__(loop)
        assert events == ["startup"]

        proto = _Protocol()
        loop.run_until_complete(app.__rsgi__(_Scope("GET", "/"), proto))
        assert proto.sent is not None
        assert msgspec.json.decode(proto.sent[2]) == {"db": "connected"}

        app.__rsgi_del__(loop)
        assert events == ["startup", "shutdown"]
    finally:
        loop.close()


def test_rsgi_no_lifespan_hooks_are_noops(app: GunbulletApp) -> None:
    loop = asyncio.new_event_loop()
    try:
        # An app without a lifespan must tolerate the hooks Granian always calls.
        app.__rsgi_init__(loop)
        app.__rsgi_del__(loop)
    finally:
        loop.close()


def test_rsgi_lifespan_startup_failure_propagates() -> None:
    app = GunbulletApp()

    @app.lifespan
    async def lifespan(app: GunbulletApp):  # type: ignore[no-untyped-def]
        raise RuntimeError("startup boom")
        yield  # pragma: no cover

    loop = asyncio.new_event_loop()
    try:
        with pytest.raises(RuntimeError, match="startup boom"):
            app.__rsgi_init__(loop)
        # Startup never completed, so shutdown must be a no-op (not exit a
        # context manager that failed to enter).
        app.__rsgi_del__(loop)
    finally:
        loop.close()
