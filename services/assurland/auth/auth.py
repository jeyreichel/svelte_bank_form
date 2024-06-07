from database.db import firestore_db
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


def does_api_key_exist(api_key: str) -> bool:
    doc = firestore_db.collection("keys").document(api_key).get()
    return doc.exists


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Gets the API key from the X-API-Key header.
    Checks if the provided API key exists in the database.
    If it does, returns the API key.
    If not, raises an HTTPException with 401 Unauthorized status.
    """

    if does_api_key_exist(api_key_header):
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
