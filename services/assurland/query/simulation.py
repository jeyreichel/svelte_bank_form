from common.models.simulation import Assure, Pret, Simulation
from database.db import firestore_db
from models.input import Adhesion as AdhesionInput


def update_with_adhesion(adhesion: AdhesionInput) -> Simulation:
    collection_ref = (
        firestore_db.collection("simulations")
        .document(adhesion.id_simulation)
        .collection("assures")
    )
    assures_docs = collection_ref.stream()
    for assure_doc in assures_docs:
        adhesion_dict = adhesion.coordonnees.model_dump()
        firestore_db.collection("simulations").document(
            adhesion.id_simulation
        ).collection("assures").document(assure_doc.id).update(adhesion_dict)
        break

    doc = firestore_db.collection("simulations").document(adhesion.id_simulation).get()
    assures_ref = (
        firestore_db.collection("simulations")
        .document(adhesion.id_simulation)
        .collection("assures")
    )
    assures_docs = assures_ref.stream()

    prets_ref = (
        firestore_db.collection("simulations")
        .document(adhesion.id_simulation)
        .collection("prets")
    )
    prets_docs = prets_ref.stream()

    assures_data = [Assure(**assure.to_dict()) for assure in assures_docs]
    prets_data = [Pret(**pret_doc.to_dict()) for pret_doc in prets_docs]
    if doc.exists:
        simulation = Simulation(
            id=doc.id, assures=assures_data, prets=prets_data, **doc.to_dict()
        )
        return simulation
    else:
        return None
