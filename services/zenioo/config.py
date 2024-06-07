from enum import Enum

from decouple import config


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


ENVIRONMENT: Environment = config(
    "ENVIRONMENT", cast=Environment, default=Environment.DEVELOPMENT
)

ZENIOO_PORT: int = config("ZENIOO_PORT", cast=int)

ZENIOO_API_URL: str = config("ZENIOO_API_URL")

CLE_PARTENAIRE_ZENIOO: str = config("CLE_PARTENAIRE_ZENIOO")
CODE_PARTENAIRE_ZENIOO: str = config("CODE_PARTENAIRE_ZENIOO")
LOGIN_COURTIER_ZENIOO: str = config("LOGIN_COURTIER_ZENIOO")
CODE_COURTIER_ZENIOO: str = config("CODE_COURTIER_ZENIOO")

PRODUCTS = [
    ("MP10", "GENERALI", "GENERALI ADE 7350 CRD"),
    ("MP20", "SWISS LIFE", "ADE SWL 1056 CRD"),
    ("MP30", "AXA", "AXA 4082 CRD"),
    ("MP40", "HARMONIE MUTUELLE", "Gar. Emp. Harmonie Mutuelle"),
    ("MP60", "MNCAP", "MNCAP ADE 0528"),
    ("MP70", "MNCAP", "MNCAP ADE 1021 CRD"),
    ("MP80", "MNCAP", "MNCAP ADE 1021 CI"),
    ("MP90", "MNCAP", "MNCAP ADE 0124 CRD"),
]
