# pylint: disable=wildcard-import,unused-wildcard-import

from .base import *
from .rest_framework import *
from .simple_jwt import *
from .emails import *
from .celery import *

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
            "level": "DEBUG",
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
            "level": "DEBUG",
        },
    },
}
