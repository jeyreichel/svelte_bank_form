from dataclasses import dataclass

import routes.adhesion
import routes.simulation
import sentry_sdk
import uvicorn
from __version__ import __version__
from config import BACKEND_PORT, ENVIRONMENT, Environment
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

sentry_sdk.init(
    release=__version__,
    environment=ENVIRONMENT.value,
)

app = FastAPI(
    title="Backend API",
    version=__version__,
    contact={
        "name": "Inekto",
        "url": "https://www.inekto.fr",
        "email": "contact@inekto.fr",
    },
)

Instrumentator().instrument(
    app, metric_namespace="techfin", metric_subsystem="backend"
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


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # todo:change origin
    allow_origins=["*"],  # Allow this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
# routing
app.include_router(routes.simulation.router)
app.include_router(routes.adhesion.router)


def run():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=(ENVIRONMENT == Environment.DEVELOPMENT),
    )
