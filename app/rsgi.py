"""
Simple RSGI Web Application

A basic RSGI application (Granian's native interface) demonstrating:
- RSGI interface: application(scope, protocol)
- Request handling and routing
- HTML response generation

Unlike ASGI's (scope, receive, send), RSGI passes a `scope` object whose
request metadata is accessed as attributes (scope.path, scope.method, ...)
and a `protocol` object that both yields the request body (await protocol())
and emits the response (protocol.response_str / response_bytes / ...).
"""


async def application(scope, protocol):
    """
    Main RSGI application with basic routing

    Args:
        scope: Object with connection/request info (proto, path, method, ...)
        protocol: Object to read the request body and send the response
    """
    # Only handle HTTP requests; ignore websockets and anything else.
    if scope.proto != "http":
        return

    path = scope.path

    # Simple routing
    if path == "/":
        await home_page(scope, protocol)
    elif path == "/about":
        await about_page(scope, protocol)
    elif path == "/contact":
        await contact_page(scope, protocol)
    else:
        await not_found_page(scope, protocol)


def send_html(protocol, status, body):
    """Emit an HTML response through the RSGI protocol object."""
    response_bytes = body.encode("utf-8")
    headers = [
        ("content-type", "text/html; charset=utf-8"),
        ("content-length", str(len(response_bytes))),
    ]

    protocol.response_bytes(status, headers, response_bytes)


async def home_page(scope, protocol):
    """Home page handler"""
    print("scope")
    print(scope)

    print(dir(scope))
    print(protocol)

    print(dir(protocol))
    method = scope.method
    path = scope.path
    query_string = scope.query_string

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple RSGI App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .info {{ background: #f0f0f0; padding: 15px; margin: 15px 0; border-radius: 5px; }}
            nav {{ margin: 20px 0; }}
            nav a {{ margin-right: 15px; color: #007acc; text-decoration: none; }}
            nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Welcome to Simple RSGI App</h1>

        <div class="info">
            <h3>Request Information:</h3>
            <p><strong>Method:</strong> {method}</p>
            <p><strong>Path:</strong> {path}</p>
            <p><strong>Query String:</strong> {query_string}</p>
        </div>

        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>

        <p>This is a simple RSGI web application demonstrating basic concepts.</p>
    </body>
    </html>
    """

    send_html(protocol, 200, body)


async def about_page(scope, protocol):
    """About page handler"""
    body = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - Simple RSGI App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            nav { margin: 20px 0; }
            nav a { margin-right: 15px; color: #007acc; text-decoration: none; }
            nav a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>About This Application</h1>

        <p>This is a simple RSGI web application that demonstrates:</p>
        <ul>
            <li>RSGI application interface</li>
            <li>Basic URL routing</li>
            <li>Request/Response handling</li>
            <li>HTML generation</li>
        </ul>

        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>
    </body>
    </html>
    """

    send_html(protocol, 200, body)


async def contact_page(scope, protocol):
    """Contact page handler"""
    body = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact - Simple RSGI App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            nav { margin: 20px 0; }
            nav a { margin-right: 15px; color: #007acc; text-decoration: none; }
            nav a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Contact Us</h1>

        <p>Get in touch with us:</p>
        <p><strong>Email:</strong> contact@example.com</p>
        <p><strong>Phone:</strong> (555) 123-4567</p>

        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>
    </body>
    </html>
    """

    send_html(protocol, 200, body)


async def not_found_page(scope, protocol):
    """404 error page handler"""
    path = scope.path

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; }}
            .error {{ color: #dc3545; }}
            nav {{ margin: 20px 0; }}
            nav a {{ margin-right: 15px; color: #007acc; text-decoration: none; }}
            nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1 class="error">404 - Page Not Found</h1>
        <p>The page <code>{path}</code> could not be found.</p>

        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>
    </body>
    </html>
    """

    send_html(protocol, 404, body)
