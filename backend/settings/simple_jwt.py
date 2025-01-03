from datetime import timedelta
import environ

env = environ.Env()
environ.Env.read_env()

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
}
