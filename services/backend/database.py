import firebase_admin
from common.models.result import Formule, Result, SimulationResponse
from common.models.simulation import Assure, Pret, Simulation
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/firestore_credentials.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()


def create(simulation: Simulation, results: list[Result]) -> SimulationResponse:
    doc_ref = firestore_db.collection("simulations").document()
    simulation_id = doc_ref.id
    doc_ref.set(simulation.model_dump(mode="json", exclude={"assures", "prets"}))

    assure_index = 1
    assure_coll = doc_ref.collection("assures")
    for assure in simulation.assures:
        assures_ref = assure_coll.document("assure" + str(assure_index))
        assures_ref.set(assure.model_dump(mode="json"))
        assure_index += 1

    pret_index = 1
    prets_coll = doc_ref.collection("prets")
    for pret in simulation.prets:
        prets_ref = prets_coll.document("pret" + str(pret_index))
        prets_ref.set(pret.model_dump(mode="json"))
        pret_index += 1

    formules = []
    results_ref = doc_ref.collection("results")
    for result in results:
        result_doc = results_ref.document()
        result_doc.set(result.model_dump(mode="json"))
        formule = Formule(
            garantie=result.garantie.value,
            compagnie=result.compagnie,
            nom_formule=result.nom,
            id_formule=result_doc.id,
            cout_total_sans_frais=result.tarif,
        )
        formules.append(formule)

    return SimulationResponse(id_simulation=simulation_id, formules=formules)


def get(simulation_id: str) -> Simulation:
    doc_ref = firestore_db.collection("simulations").document(simulation_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise KeyError

    assures_docs = doc_ref.collection("assures").stream()
    assures_data = [Assure(**assure.to_dict()) for assure in assures_docs]

    prets_docs = doc_ref.collection("prets").stream()
    prets_data = [Pret(**pret_doc.to_dict()) for pret_doc in prets_docs]

    return Simulation(assures=assures_data, prets=prets_data, **doc.to_dict())


def get_response(simulation_id: str) -> SimulationResponse:
    simulation = firestore_db.collection("simulations").document(simulation_id)
    if not simulation.get().exists:
        raise KeyError
    results = simulation.collection("results").stream()
    formules = []
    for result_doc in results:
        result = result_doc.to_dict()
        formule = Formule(
            garantie=result["garantie"],
            compagnie=result["compagnie"],
            nom_formule=result["nom"],
            id_formule=result_doc.id,
            cout_total_sans_frais=result["tarif"],
        )
        formules.append(formule)
    return SimulationResponse(id_simulation=simulation_id, formules=formules)


def get_simulation_result_by_id(
    id_simulation: str, id_result: str
) -> tuple[Simulation | None, Result | None]:
    doc_ref = firestore_db.collection("simulations").document(id_simulation)
    doc = doc_ref.get()

    assures_ref = (
        firestore_db.collection("simulations")
        .document(id_simulation)
        .collection("assures")
    )
    assures_docs = assures_ref.stream()

    prets_ref = (
        firestore_db.collection("simulations")
        .document(id_simulation)
        .collection("prets")
    )
    prets_docs = prets_ref.stream()

    assures_data = [Assure(**assure.to_dict()) for assure in assures_docs]
    prets_data = [Pret(**pret_doc.to_dict()) for pret_doc in prets_docs]
    if not doc.exists:
        return None, None
    simulation = Simulation(assures=assures_data, prets=prets_data, **doc.to_dict())

    doc_ref = doc_ref.collection("results").document(id_result)
    doc = doc_ref.get()
    if not doc.exists:
        return simulation, None
    result = Result(**doc.to_dict())
    return simulation, result


def update_result_url(id_simulation: str, id_result: str, url: str) -> Result:
    results_ref = (
        firestore_db.collection("simulations")
        .document(id_simulation)
        .collection("results")
    )
    result_ref = results_ref.document(id_result)
    doc = result_ref.get()
    results_ref.document(id_result).update({"url": url})
    if doc.exists:
        return Result(**doc.to_dict())
    raise KeyError
