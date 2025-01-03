import environ

env = environ.Env()
environ.Env.read_env()

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "")

# Cache settings using Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
