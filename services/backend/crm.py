from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import assert_never
from loguru import logger
from hubspot import HubSpot
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate as ContactInputForCreate,
    SimplePublicObjectInput as ContactInput,
    PublicObjectSearchRequest as ContactSearchInput,
    FilterGroup as ContactFilterGroup,
    Filter as ContactFilter,
)
from hubspot.crm.contacts.exceptions import ApiException
from hubspot.crm.deals import (
    SimplePublicObjectInputForCreate as DealInput,
    PublicAssociationsForObject as DealAssociation,
    AssociationSpec as DealAssociationSpec,
    PublicObjectSearchRequest as DealSearchInput,
    FilterGroup as DealFilterGroup,
    Filter as DealFilter,
)
from hubspot.crm.line_items import (
    SimplePublicObjectId as LineItemSimplePublicObjectId,
    SimplePublicObjectBatchInput as LineItemSimplePublicObjectBatchInput,
    BatchReadInputSimplePublicObjectId as LineItemBatchReadInputSimplePublicObjectId,
    BatchInputSimplePublicObjectBatchInput as BatchLineItemObjectInput,
    SimplePublicObjectInputForCreate as LineItemInputForCreate,
    BatchInputSimplePublicObjectInputForCreate as BatchLineItemInputForCreate,
)

from config import HUBSPOT_KEY
from common.models.simulation import Assure, ObjetPret, Simulation, Origin
from common.models.result import Formule, SimulationResponse

api_client = HubSpot(access_token=HUBSPOT_KEY)


def valid_assure(assure: Assure) -> bool:
    return (
        assure.prenom is not None
        and assure.nom is not None
        and assure.email is not None
        and assure.email is not None
    )


def search_contact(email: str) -> str:
    """Search for an existing contact in Hubspot based on the email address

    Args:
        email (str): the email to look for in Hubspot

    Raises:
        KeyError: there is no contact with that email
        ApiException: an exception occured when calling the Hubspot API

    Returns:
        str: the ID of the corresponding contact in Hubspot
    """
    search_request = ContactSearchInput(
        filter_groups=[
            ContactFilterGroup(
                filters=[
                    ContactFilter(property_name="email", operator="EQ", value=email)
                ]
            )
        ],
        limit=1,
        properties=["id"],
    )
    try:
        api_response = api_client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )
        if api_response.results == []:
            raise KeyError
        else:
            return api_response.results[0].id
    except ApiException as e:
        logger.error("Exception when searching contact: %s\n" % e)
        raise e


def update_contact(origin: Origin, assure: Assure) -> str | None:
    """Creates contacts in Hubspot for each assure in the input list.
       If contacts already exist with the same email address, they are updated.

    Args:
        origin (Origin): the origin of the contact
        assure (list[Assure]): the assures we should build contacts from. The object
                               should contain the full information (no None members)

    Raises:
        ApiException: an exception occured when calling the Hubspot API

    Returns:
        list[str]: the IDs of the created contacts
    """
    # Build the contact information we want to upload
    properties = {
        "gender": assure.genre.value,
        "date_of_birth": assure.date_naissance.isoformat(),
        "job_function": assure.profession.value,
        "deplacements_professionels": assure.deplacements_pro.value,
        "travaux_manuels": assure.travaux_manuels.value,
        "fumeur": assure.fumeur,
        "quotite": assure.quotite / 100,
        "lastname": assure.nom,
        "firstname": assure.prenom,
        "address": assure.adresse,
        "zip": assure.code_postal,
        "city": assure.ville,
        "phone": assure.telephone,
        "email": assure.email,
        "origine": origin.value,
    }

    # Look for an existing contact with this email
    try:
        # If it exists, update it
        contact_id = search_contact(assure.email)
        api_response = api_client.crm.contacts.basic_api.update(
            contact_id=contact_id,
            simple_public_object_input=ContactInput(properties=properties),
        )
    except KeyError:
        # If it does not exist, create it
        try:
            api_response = api_client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=ContactInputForCreate(
                    properties=properties
                )
            )
        except ApiException as e:
            logger.error("Exception when creating contact: %s\n" % e)
            raise e
    except ApiException as e:
        logger.error("Exception when creating contact: %s\n" % e)
        raise e
    return api_response.id


def create_products(deal_id: str, simulation: Simulation, formules: list[Formule]):
    formule_min_index = min(
        range(len(formules)), key=lambda i: formules[i].cout_total_sans_frais
    )
    montant_total = sum([pret.montant for pret in simulation.prets])
    duree_totale_ans = max([pret.duree for pret in simulation.prets]) / 12
    taux_moyen_avant_30 = 0.0026
    taux_moyen_apres_30 = 0.004
    prix_moyen = (
        duree_totale_ans
        * montant_total
        * (
            taux_moyen_avant_30
            if relativedelta(simulation.assures[0].date_naissance, date.today()).years
            < 30
            else taux_moyen_apres_30
        )
    )
    line_items = [
        LineItemInputForCreate(
            properties={
                "name": formule.nom_formule,
                "identifiant_de_formule": formule.id_formule,
                "price": formule.cout_total_sans_frais,
                "quantity": 1 if i == formule_min_index else 0,
                "economie_attendue": f"{prix_moyen - formule.cout_total_sans_frais:.2f}",
                "taux_moyen_annuel": formule.cout_total_sans_frais
                / (montant_total * duree_totale_ans),
            },
            associations=[
                DealAssociation(
                    types=[
                        DealAssociationSpec(
                            association_category="HUBSPOT_DEFINED",
                            association_type_id="20",
                        )
                    ],
                    to=deal_id,
                )
            ],
        )
        for i, formule in enumerate(formules)
    ]
    try:
        api_client.crm.line_items.batch_api.create(
            batch_input_simple_public_object_input_for_create=BatchLineItemInputForCreate(
                inputs=line_items
            )
        )
    except ApiException as e:
        logger.error("Exception when creating contact: %s\n" % e)
        raise e


def create_from_full_simulation(
    simulation: Simulation, response: SimulationResponse
) -> str:
    if all([not valid_assure(assure) for assure in simulation.assures]):
        logger.info("Missing information: ignoring the simulation")
        return

    match simulation.objet_pret:
        case ObjetPret.RESIDENCE_PRINCIPALE:
            objet_court = "RP"
        case ObjetPret.RESIDENCE_SECONDAIRE:
            objet_court = "RL"
        case ObjetPret.INVESTISSEMENT_LOCATIF:
            objet_court = "IL"
        case ObjetPret.AUTRE:
            objet_court = "AUTRE"
        case _ as unreachable:
            assert_never(unreachable)
    dealname = (
        f"{simulation.assures[0].prenom} {simulation.assures[0].nom} ({objet_court})"
    )
    logger.info(f"Creating Hubspot contacts for simulation {response.id_simulation}")

    emprunteurs_ids = [
        update_contact(origin=simulation.origin, assure=assure)
        for assure in simulation.assures
        if valid_assure(assure)
    ]

    deal = DealInput(
        properties={
            "pipeline": "default",
            "dealstage": "appointmentscheduled",
            "dealname": dealname,
            "identifiant_de_simulation": response.id_simulation,
            "closedate": (date.today() + timedelta(days=90)).isoformat(),
            "amount": min(
                [result.cout_total_sans_frais for result in response.formules]
            ),
            "banque": simulation.banque.value,
            "origine": simulation.origin.value,
        },
        associations=[
            DealAssociation(
                types=[
                    # Emprunteur
                    DealAssociationSpec(
                        association_category="USER_DEFINED",
                        association_type_id="5",
                    )
                ],
                to=id,
            )
            for id in emprunteurs_ids
        ],
    )
    try:
        logger.info(f"Creating Hubspot deal for simulation {response.id_simulation}")
        api_response = api_client.crm.deals.basic_api.create(
            simple_public_object_input_for_create=deal
        )
        deal_id = api_response.id
        create_products(deal_id, simulation, response.formules)
        return deal_id
    except ApiException as e:
        logger.error("Exception when creating deal: %s\n" % e)
        raise e


def search_deal(simulation_id: str) -> str:
    search_request = DealSearchInput(
        filter_groups=[
            DealFilterGroup(
                filters=[
                    DealFilter(
                        property_name="identifiant_de_simulation",
                        operator="EQ",
                        value=simulation_id,
                    )
                ]
            )
        ],
        limit=1,
    )
    try:
        api_response = api_client.crm.deals.search_api.do_search(
            public_object_search_request=search_request
        )
        if api_response.results == []:
            raise KeyError
        else:
            return api_response.results[0].id
    except ApiException as e:
        logger.error(f"Error when searching deal {simulation_id}")
        raise e


def get_products(deal_id: str):
    try:
        api_response = api_client.crm.deals.basic_api.get_by_id(
            deal_id, properties=[], associations=["line_items"]
        )
        products = [
            LineItemSimplePublicObjectId(id=line_item.id)
            for line_item in api_response.associations["line items"].results
        ]
        batch = LineItemBatchReadInputSimplePublicObjectId(
            inputs=products, properties=["identifiant_de_formule"]
        )

        api_response = api_client.crm.line_items.batch_api.read(
            batch_read_input_simple_public_object_id=batch
        )
        products = [
            (result.id, result.properties["identifiant_de_formule"])
            for result in api_response.results
        ]
        return products
    except ApiException as e:
        logger.error(f"Error when retrieving products associated with {deal_id}")
        raise e


def upgrade_products(deal_id: str, subscribed_formule: str):
    line_items = get_products(deal_id)
    line_items_upgrades = [
        LineItemSimplePublicObjectBatchInput(
            id=hubspot_id,
            properties={
                "quantity": 1 if formule_id == subscribed_formule else 0,
            },
        )
        for (hubspot_id, formule_id) in line_items
    ]
    try:
        api_client.crm.line_items.batch_api.update(
            batch_input_simple_public_object_batch_input=BatchLineItemObjectInput(
                inputs=line_items_upgrades
            )
        )
    except ApiException as e:
        logger.error(f"Exception when upgrading products {e}")
        raise e


def upgrade_to_qualified(deal_id: str, formule_id: str, url: str, amount: float):
    deal = DealInput(
        properties={
            "dealstage": "qualifiedtobuy",
            "lien_de_souscription": url,
            "amount": amount,
        },
    )
    try:
        upgrade_products(deal_id, formule_id)
        api_client.crm.deals.basic_api.update(deal_id, simple_public_object_input=deal)
    except ApiException as e:
        logger.error("Exception when upgrading deal: %s\n" % e)
        raise e
