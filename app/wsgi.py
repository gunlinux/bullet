"""
Simple WSGI Web Application

A basic WSGI application demonstrating:
- WSGI interface: application(environ, start_response)
- Request handling and routing
- HTML response generation
"""


def application(environ, start_response):
    """
    Main WSGI application with basic routing

    Args:
        environ: Dictionary with request information
        start_response: Function to set response status and headers

    Returns:
        List of bytes (response body)
    """
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]

    # Simple routing
    if path == "/":
        return home_page(environ, start_response)
    elif path == "/about":
        return about_page(environ, start_response)
    elif path == "/contact":
        return contact_page(environ, start_response)
    else:
        return not_found_page(environ, start_response)


def home_page(environ, start_response):
    """Home page handler"""
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]

    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    query_string = environ.get("QUERY_STRING", "")

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple WSGI App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .info {{ background: #f0f0f0; padding: 15px; margin: 15px 0; border-radius: 5px; }}
            nav {{ margin: 20px 0; }}
            nav a {{ margin-right: 15px; color: #007acc; text-decoration: none; }}
            nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Welcome to Simple WSGI App</h1>
        
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
        
        <p>This is a simple WSGI web application demonstrating basic concepts.</p>
    </body>
    </html>
    """

    response_bytes = body.encode("utf-8")
    headers.append(("Content-Length", str(len(response_bytes))))

    start_response(status, headers)
    return [response_bytes]


def about_page(environ, start_response):
    """About page handler"""
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]

    body = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - Simple WSGI App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            nav { margin: 20px 0; }
            nav a { margin-right: 15px; color: #007acc; text-decoration: none; }
            nav a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>About This Application</h1>
        
        <p>This is a simple WSGI web application that demonstrates:</p>
        <ul>
            <li>WSGI application interface</li>
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

    response_bytes = body.encode("utf-8")
    headers.append(("Content-Length", str(len(response_bytes))))

    start_response(status, headers)
    return [response_bytes]


def contact_page(environ, start_response):
    """Contact page handler"""
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]

    body = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact - Simple WSGI App</title>
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

    response_bytes = body.encode("utf-8")
    headers.append(("Content-Length", str(len(response_bytes))))

    start_response(status, headers)
    return [response_bytes]


def not_found_page(environ, start_response):
    """404 error page handler"""
    status = "404 Not Found"
    headers = [("Content-Type", "text/html; charset=utf-8")]

    path = environ.get("PATH_INFO", "/")

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

    response_bytes = body.encode("utf-8")
    headers.append(("Content-Length", str(len(response_bytes))))

    start_response(status, headers)
    return [response_bytes]


