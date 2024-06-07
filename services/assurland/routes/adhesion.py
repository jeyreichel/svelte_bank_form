import httpx
import query.simulation
from auth.auth import get_api_key
from config import BACKEND_URL
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from models.input import Adhesion
from models.output import AdhesionResponse
from pydantic import BaseModel

router = APIRouter()
client = httpx.AsyncClient()


class AdhesionId(BaseModel):
    id_simulation: str
    id_result: str


@router.post("/adhesion")
async def adhesion(adhesion: Adhesion, api_key: str = Depends(get_api_key)):
    logger.info("Recieved subscription request, updating customer info in database")
    query.simulation.update_with_adhesion(adhesion)
    adhesion_id = AdhesionId(
        id_simulation=adhesion.id_simulation, id_result=adhesion.id_formule
    )
    response = await client.post(
        f"{BACKEND_URL}/adhesion", content=adhesion_id.model_dump_json(), timeout=30
    )
    if response.status_code == httpx.codes.OK:
        response = AdhesionResponse(
            url="https://www.omeros.fr/comparateur-assurland-mncap"
        )
        return response
    else:
        detail = response.json()["detail"]
        logger.error(f"Backend failed to process the subscription: {detail}")
        raise HTTPException(response.status_code, detail)
