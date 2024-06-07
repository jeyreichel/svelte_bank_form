import httpx
from common.models.result import AdhesionResponse
from common.models.simulation import SimulationWithTarif
from config import PROVIDERS
import database
from database import get_simulation_result_by_id, update_result_url
from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel
import crm

client = httpx.AsyncClient()


class AdhesionId(BaseModel):
    id_simulation: str
    id_result: str


router = APIRouter()


@router.post("/adhesion")
async def adhesion(adhesion: AdhesionId):
    logger.info(
        f"Recieved adhesion request for simulation {adhesion.id_simulation} (result {adhesion.id_result})"
    )
    simulation, result = get_simulation_result_by_id(
        adhesion.id_simulation, adhesion.id_result
    )
    if simulation is None:
        logger.info(f"Simulation {adhesion.id_simulation} does not exist")
        raise HTTPException(
            status_code=404,
            detail=f"La simulation {adhesion.id_simulation} n'a pas été trouvée",
        )
    if result is None:
        logger.info(f"Result {adhesion.id_result} does not exist")
        raise HTTPException(
            status_code=404,
            detail=f"La formule {adhesion.id_result} n'a pas été trouvée",
        )
    simulation_with_tarif = SimulationWithTarif(
        simulation=simulation, id_tarif=result.id_tarif
    )

    origin = result.origin
    origin_url = PROVIDERS[result.origin]

    logger.info(f"Sending adhesion request to {origin} @ {origin_url}")
    response = await client.post(
        f"{origin_url}/adhesion",
        content=simulation_with_tarif.model_dump_json(),
        timeout=30,
    )
    if response.status_code == 200:
        logger.info(f"Recieved response from {origin}")
        adhesion_result = response.json()
        url = adhesion_result["url"]
        update_result_url(adhesion.id_simulation, adhesion.id_result, url)

        # CRM Updates
        try:
            deal_id = crm.search_deal(adhesion.id_simulation)
        except KeyError:
            simulation_response = database.get_response(adhesion.id_simulation)
            deal_id = crm.create_from_full_simulation(simulation, simulation_response)
        crm.upgrade_to_qualified(deal_id, adhesion.id_result, url, result.tarif)
        return AdhesionResponse(url=url)

    raise HTTPException(
        status_code=422,
        detail="L'adhésion a été refusée par le fournisseur",
    )
