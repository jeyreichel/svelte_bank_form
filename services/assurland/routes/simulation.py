import converter
import httpx
from auth.auth import get_api_key
from common.models.result import SimulationResponse as BackendSimulationResponse
from common.models.simulation import Simulation
from config import BACKEND_URL
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from models.input import Simulation as SimulationInput
from models.output import Formule, SimulationResponse

router = APIRouter()

client = httpx.AsyncClient()


@router.post("/simulation")
async def simulation(
    simulation_input: SimulationInput, api_key: str = Depends(get_api_key)
):
    logger.info("Recieved simulation request, forwarding to backend")
    simulation: Simulation = converter.simulation(simulation_input)
    response = await client.post(
        f"{BACKEND_URL}/simulation",
        content=simulation.model_dump_json(),
        timeout=30,
    )
    if response.is_server_error:
        logger.warning("Backend critical failure")
        raise HTTPException(status_code=500)
    if response.is_client_error:
        detail = response.json()["detail"]
        raise HTTPException(status_code=response.status_code, detail=detail)
    if response.is_success:
        logger.info("Recieved quotes from backend")
        montant_total = sum([pret.montant for pret in simulation.prets])
        duree_totale = max([pret.duree for pret in simulation.prets])
        response = BackendSimulationResponse(**response.json())
        formules = []
        for formule in response.formules:
            if formule.nom_formule in [
                "MNCAP ADE 1021 CI",
                "MNCAP ADE 1021 CRD",
                "AXA 4082 CRD",
            ]:
                mensualite = formule.cout_total_sans_frais / duree_totale
                formule = Formule(
                    prime_premiere_annee=12 * mensualite,
                    premiere_mensualite=mensualite,
                    taux_moyen_annuel=formule.cout_total_sans_frais
                    / (montant_total * duree_totale / 12)
                    * 100,
                    frais=70,
                    **formule.model_dump(),
                )
                formules.append(formule)
        response = SimulationResponse(
            formules=formules, id_simulation=response.id_simulation
        )
        return response
    else:
        logger.error("Simulation failure")
        try:
            detail = response.json()["detail"]
        except BaseException:
            detail = None
        raise HTTPException(status_code=response.status_code, detail=detail)
