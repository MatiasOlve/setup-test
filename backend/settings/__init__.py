import environ


env = environ.Env()
environ.Env.read_env()
ENVIRONMENT = env.str("DJANGO_ENV", "development")

if ENVIRONMENT == "development":
    from .development import *

if ENVIRONMENT == "production":
    from .production import *
