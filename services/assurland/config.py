from enum import Enum

from decouple import config


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


ENVIRONMENT = config("ENVIRONMENT", cast=Environment, default=Environment.DEVELOPMENT)

BACKEND_PORT = config("BACKEND_PORT", cast=int)

BACKEND_HOST = config("BACKEND_HOST")
BACKEND_PORT = config("BACKEND_PORT", cast=int)
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

ASSURLAND_HOST = config("ASSURLAND_HOST")
ASSURLAND_PORT = config("ASSURLAND_PORT", cast=int)
ASSURLAND_URL = f"http://{ASSURLAND_HOST}:{ASSURLAND_PORT}"
