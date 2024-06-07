import asyncio

import database
import httpx
from common.models.result import Result, SimulationWithResponse
from common.models.simulation import Origin, Simulation
import crm
from config import PROVIDERS
from fastapi import APIRouter, HTTPException
from loguru import logger

router = APIRouter()

client = httpx.AsyncClient()


@router.post("/simulation")
async def simulation(simulation: Simulation):
    logger.info("Recieved simulation request for simulation")

    results = []

    async def send_request(origin, origin_url):
        logger.info(f"Sending simulation request to {origin} @ {origin_url}")
        try:
            response = await client.post(
                f"{origin_url}/simulation",
                content=simulation.model_dump_json(),
                timeout=30,
            )
        except httpx.ConnectError:
            logger.critical(f"{origin} service is down")
            return
        if response.is_server_error:
            logger.error(f"{origin} critical failure")
            return
        if response.is_client_error:
            logger.warning(f"{origin} refused the simulation")
            return
        logger.info(f"Saving {origin} responses")

        for response in response.json():
            result = Result(**response)
            logger.debug(
                f"Saving tarif {result.id_tarif} ({result.nom}) recieved from {origin}"
            )
            results.append(result)

    processes = [send_request(name, url) for name, url in PROVIDERS.items()]
    await asyncio.gather(*processes)

    response = database.create(simulation, results)

    if simulation.origin != Origin.ASSURLAND and results != []:
        crm.create_from_full_simulation(simulation, response)

    return response


@router.get("/simulation/{id_simulation}")
async def get_simulation(id_simulation: str):
    logger.info(f"Recieved simulation detail request for simulation {id_simulation}")
    try:
        simulation = database.get(id_simulation)
        response = database.get_response(id_simulation)
        return SimulationWithResponse(simulation=simulation, response=response)
    except KeyError:
        raise HTTPException(status_code=404, detail="Simulation not found")
