from app.wsgi import application as wsgi_app
from app.asgi import application as asgi_app
from app.rsgi import application as rsgi_app


def create_app_wsgi():
    return wsgi_app

def create_app_asgi():
    return asgi_app

def create_app_rsgi():
    return rsgi_app

