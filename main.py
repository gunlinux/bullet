import logging

# Configure logging before importing the app so anything logged at import time
# is captured by this config rather than the default lastResort handler.
logging.basicConfig(level=logging.INFO)

from app import create_app_asgi  # noqa: E402

app_asgi = create_app_asgi()
