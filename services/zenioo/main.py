import asyncio
from dataclasses import dataclass
from typing import List

import sentry_sdk
import uvicorn
from api import get_data_for_zenioo, send_simulation, send_subscription
from common.__version__ import __version__
from common.models.result import AdhesionResponse, Result
from common.models.simulation import Simulation, SimulationWithTarif
from config import ENVIRONMENT, ZENIOO_PORT, Environment, PRODUCTS
from fastapi import FastAPI, HTTPException, status
from loguru import logger
from models import PackageGaranties
from prometheus_fastapi_instrumentator import Instrumentator
from to_zenioo_api import banque, to_zenioo_api

sentry_sdk.init(
    release=__version__,
    environment=ENVIRONMENT.value,
)

app = FastAPI(
    title="Zenioo API",
    version=__version__,
    contact={
        "name": "Inekto",
        "url": "https://www.inekto.fr",
        "email": "contact@inekto.fr",
    },
)

Instrumentator().instrument(
    app, metric_namespace="techfin", metric_subsystem="zenioo"
).expose(app, include_in_schema=False)


@dataclass
class HealthCheck:
    status: str
    version: str


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK", version=__version__)


@app.post("/simulation", response_model=List[Result])
async def simulation(input_simulation: Simulation):
    logger.info("Recieved simulation request, initiating calls to external API")
    responses = []

    async def get_product(code: str, compagnie: str, nom: str):
        contrat, beneficiaires, simulation, prets, garanties = to_zenioo_api(
            input_simulation, code
        )
        new_data = get_data_for_zenioo(
            contrat, beneficiaires, simulation, prets, garanties
        )
        response = await send_simulation(new_data)
        response = response.json()
        if "erreur" not in response:
            logger.debug(f"Recieved a response for product {code}")
            result = Result(
                nom=nom,
                compagnie=compagnie,
                tarif=float(response["Tarif_global"]["cotisation_totale"]),
                id_tarif=response["Produit"]["code_produit"],
                garantie=PackageGaranties(
                    response["Produit"]["libelle_formule_long"]
                ).from_zenioo(),
                origin="zenioo",
            )
            logger.debug(f"Successfully processed response for product {code}")
            responses.append(result)
        else:
            logger.warning(
                f"Response for tarif {code} could not be processed: {response}"
            )
            pass

    processes = [
        get_product(code, compagnie, nom) for (code, compagnie, nom) in PRODUCTS
    ]
    await asyncio.gather(*processes)
    logger.info("Responded to simulation request")
    return responses


@app.post("/adhesion")
async def adhesion(data: SimulationWithTarif):
    logger.info("Recieved subscription request, initiating call to external API")
    contrat, beneficiaires, simulation, prets, garanties = to_zenioo_api(
        data.simulation, data.id_tarif
    )
    new_data = get_data_for_zenioo(contrat, beneficiaires, simulation, prets, garanties)
    new_data["organisme_preteur"] = [banque(data.simulation.banque)]
    response = await send_subscription(new_data)
    response = response.json()
    if response["response"]["codeErreur"] != "200":
        logger.error(f"Subscription request failed: {response['response']}")
        raise HTTPException(
            status_code=int(response["response"]["codeErreur"]),
            detail=response["response"]["message"],
        )
    adhesion = AdhesionResponse(
        url=response["response"]["url_zenioo"],
    )
    return adhesion


def run():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=ZENIOO_PORT,
        reload=(ENVIRONMENT == Environment.DEVELOPMENT),
    )
