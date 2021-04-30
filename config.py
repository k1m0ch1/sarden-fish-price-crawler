from os import environ

_ = environ.get

API_URL=_("API_URL", "http://127.0.0.1:8000")
ENDPOINT_SAVE_LOG=_("ENDPOINT_SAVE_LOG", "/api")
AUTH_USERNAME=_("AUTH_USERNAME", "USERNAME")
AUTH_PASSWORD=_("AUTH_PASSWORD", "PASSWORD")