import common.models.result
from pydantic import BaseModel, field_serializer


class Formule(common.models.result.Formule):
    prime_premiere_annee: float
    premiere_mensualite: float
    taux_moyen_annuel: float
    frais: float

    @field_serializer(
        "prime_premiere_annee",
        "premiere_mensualite",
        "taux_moyen_annuel",
        "frais",
        when_used="json",
    )
    def serialize_cout(self, cout: float, _info):
        return f"{cout:.2f}"


class SimulationResponse(common.models.result.SimulationResponse):
    formules: list[Formule] = []


class AdhesionResponse(BaseModel):
    url: str
