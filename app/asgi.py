"""
Simple ASGI Web Application

A basic ASGI application demonstrating:
- ASGI interface: application(scope, receive, send)
- Request handling and routing
- HTML response generation
"""

async def application(scope, receive, send):
    """
    Main ASGI application with basic routing

    Args:
        scope: Dict with connection/request info (type, path, method, ...)
        receive: Awaitable to receive ASGI events from the server
        send: Awaitable to send ASGI events back to the server
    """
    print(type(scope))
    print(type(receive))
    print(type(send))
    # Handle the lifespan protocol (startup/shutdown) so servers don't hang.
    if scope["type"] == "lifespan":
        while True:
            event = await receive()
            if event["type"] == "lifespan.startup":
                print("lifespan handler")
                await send({"type": "lifespan.startup.complete"})
            elif event["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    # Drain the request body events (we don't use the body, but must consume them).
    more_body = True
    while more_body:
        event = await receive()
        more_body = event.get("more_body", False)

    path = scope["path"]

    # Simple routing
    if path == "/":
        await home_page(scope, receive, send)
    elif path == "/about":
        await about_page(scope, receive, send)
    elif path == "/contact":
        await contact_page(scope, receive, send)
    elif path == "/api/pydantic":
        await api_pydantic_page(scope, receive, send)
    # elif path == "/api/marshmallow":
    # await api_marshmallow_page(scope, receive, send)
    elif path == "/api/marshmallow-ujson":
        await api_marshmallow_ujson_page(scope, receive, send)
    elif path == "/api/marshmallow-local":
        await api_marshmallow_local_page(scope, receive, send)
    elif path == "/api/msgspec":
        await api_msgspec_page(scope, receive, send)
    else:
        await not_found_page(scope, receive, send)


async def send_html(send, status, body):
    """Encode an HTML body and emit the ASGI response events."""
    response_bytes = body.encode("utf-8")
    headers = [
        (b"content-type", b"text/html; charset=utf-8"),
        (b"content-length", str(len(response_bytes)).encode("utf-8")),
    ]

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": headers,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": response_bytes,
        }
    )


async def send_json(send, status, body):
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
    await send(
        {
            "type": "http.response.body",
            "body": body,
        }
    )


async def home_page(scope, receive, send):
    """Home page handler"""
    method = scope["method"]
    path = scope["path"]
    query_string = scope.get("query_string", b"").decode("utf-8")


