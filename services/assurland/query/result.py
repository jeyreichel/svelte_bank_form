import models
from database.db import firestore_db


def by_simulation_id(id_simulation):
    results = (
        firestore_db.collection("simulations")
        .document(id_simulation)
        .collection("results")
    ).stream()

    results = [
        (result.id, models.result.Result(**result.to_dict())) for result in results
    ]
    return results


def url(id_simulation, id_result) -> str:
    result = (
        firestore_db.collection("simulations")
        .document(id_simulation)
        .collection("results")
        .document(id_result)
        .get()
        .to_dict()
    )
    return result["url"]


# def get_result_by_id(adhesion: AdhesionInput) -> Result:
#     doc_ref = (
#         firestore_db.collection("simulations")
#         .document(adhesion.id_simulation)
#         .collection("results")
#         .document(sanitize_string(adhesion.id_formule))
#     )
#     doc = doc_ref.get()
#     if doc.exists:
#         simulation = Result(**doc.to_dict())
#         return simulation
#     else:
#         return None


def by_name(adhesion: models.input.Adhesion):
    query = (
        firestore_db.collection("simulations")
        .document(adhesion.id_simulation)
        .collection("results")
        .where("nom", "==", adhesion.id_formule)
    )
    docs = query.stream()
    for doc in docs:
        result = models.result.Result(**doc.to_dict())
        return result, doc.id
    return None, None
