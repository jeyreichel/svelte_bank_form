import common.models.simulation
from common.models.simulation import Simulation
from models.input import Simulation as SimulationInput


def simulation(s: SimulationInput) -> Simulation:
    return Simulation(
        origin=common.models.simulation.Origin.ASSURLAND,
        banque=common.models.simulation.Banque.SOCIETE_GENERALE,
        objet_demande=common.models.simulation.ObjetDemande.NOUVEAU_PRET,
        **s.model_dump(),
    )
