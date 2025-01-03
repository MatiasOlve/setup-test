# pylint: disable=wildcard-import,unused-wildcard-import

from django.db.backends.postgresql.psycopg_any import IsolationLevel

from .base import *
from .rest_framework import *
from .simple_jwt import *
from .emails import *
from .celery import *


DATABASES["default"]["OPTIONS"] = {
    "isolation_level": IsolationLevel.SERIALIZABLE,
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None},
        },
        "TIMEOUT": 3600,  # Set cache items to expire after 1 hour (in seconds)
    }
}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": THROTTLE_RATES_ANON,
        "user": THROTTLE_RATES_USER,
    },
    "NUM_PROXIES": THROTTLE_NUM_PROXIES,
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "backend": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}
