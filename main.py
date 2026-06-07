from app import create_app_wsgi
from app import create_app_asgi
from app import create_app_rsgi
from app.users import Users

users = Users()

app_wsgi = create_app_wsgi()
app_asgi = create_app_asgi()
app_rsgi = create_app_rsgi()
