from enum import Enum

from decouple import config


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


ENVIRONMENT = config("ENVIRONMENT", cast=Environment, default=Environment.DEVELOPMENT)

BACKEND_PORT = config("BACKEND_PORT", cast=int)

ZENIOO_HOST = config("ZENIOO_HOST")
ZENIOO_PORT = config("ZENIOO_PORT")
ZENIOO_URL = f"http://{ZENIOO_HOST}:{ZENIOO_PORT}"

HUBSPOT_KEY: str = config("HUBSPOT_KEY")

PROVIDERS = {
    "zenioo": ZENIOO_URL,
}
