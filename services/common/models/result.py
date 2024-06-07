from pydantic import BaseModel, field_serializer

from common.models.simulation import Garantie, Simulation


class Result(BaseModel):
    tarif: float
    compagnie: str
    nom: str
    garantie: Garantie
    id_tarif: str
    origin: str


class ResultInputUrl(BaseModel):
    url: str


class Formule(BaseModel):
    garantie: str
    nom_formule: str
    compagnie: str
    id_formule: str
    cout_total_sans_frais: float

    @field_serializer("cout_total_sans_frais", when_used="json")
    def serialize_cout(self, cout: float, _info):
        return f"{cout:.2f}"


class SimulationResponse(BaseModel):
    id_simulation: str
    formules: list[Formule] = []


class SimulationWithResponse(BaseModel):
    simulation: Simulation
    response: SimulationResponse


class AdhesionResponse(BaseModel):
    url: str
