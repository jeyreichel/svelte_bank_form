import datetime

import common.models.simulation as back
import faker
from common.models.simulation import (
    Assure,
    DeplacementsPro,
    Genre,
    ObjetDemande,
    ObjetPret,
    Pret,
    Profession,
    Simulation,
    TravauxManuels,
    TypePret,
)
from models import PackageGaranties

faker = faker.Faker("fr_FR")


def _to_zenioo_date(date: datetime.date):
    return date.strftime("%Y-%m-%d")


def banque(b: back.Banque):
    mapping = {
        back.Banque.CREDIT_AGRICOLE: {
            "id_organisme_preteur": "18206",
            "raison_sociale": "CREDIT AGRICOLE ILE DE FRANCE",
        },
        back.Banque.CAISSE_EPARGNE: {
            "id_organisme_preteur": "17515",
            "raison_sociale": "CAISSE D'EPARGNE ILE-DE-FRANCE",
        },
        back.Banque.SOCIETE_GENERALE: {
            "id_organisme_preteur": "30003",
            "raison_sociale": "SOCIETE GENERALE",
        },
        back.Banque.BNP: {
            "id_organisme_preteur": "30004",
            "raison_sociale": "BNP PARIBAS",
        },
        back.Banque.CREDIT_MUTUEL: {
            "id_organisme_preteur": "10278",
            "raison_sociale": "CREDIT MUTUEL",
        },
        back.Banque.LCL: {"id_organisme_preteur": "30002", "raison_sociale": "LCL"},
        back.Banque.BANQUE_POPULAIRE: {
            "id_organisme_preteur": "10207",
            "raison_sociale": "BANQUE POPULAIRE RIVES DE PARIS",
        },
        back.Banque.LA_BANQUE_POSTALE: {
            "id_organisme_preteur": "20041001",
            "raison_sociale": "LA BANQUE POSTALE - avant " "07/12/2022",
        },
        back.Banque.CIC: {"id_organisme_preteur": "30066", "raison_sociale": "CIC"},
        back.Banque.CREDIT_DU_NORD: {
            "id_organisme_preteur": "30076",
            "raison_sociale": "CREDIT DU NORD",
        },
        back.Banque.AXA: {
            "id_organisme_preteur": "12548",
            "raison_sociale": "AXA BANQUE",
        },
        back.Banque.BRED: {
            "id_organisme_preteur": "10107",
            "raison_sociale": "BRED BANQUE POPULAIRE",
        },
        back.Banque.FORTUNEO: {
            "id_organisme_preteur": "14518",
            "raison_sociale": "FORTUNEO",
        },
        back.Banque.BOURSORAMA: {
            "id_organisme_preteur": "40618",
            "raison_sociale": "BOURSOBANK",
        },
        back.Banque.HELLOBANK: {
            "id_organisme_preteur": "30004",
            "raison_sociale": "BNP PARIBAS",
        },
        back.Banque.GROUPAMA: {
            "id_organisme_preteur": "99999",
            "raison_sociale": "Groupama",
        },
        back.Banque.HSBC: {"id_organisme_preteur": "30056", "raison_sociale": "HSBC"},
        back.Banque.ING: {"id_organisme_preteur": "30438", "raison_sociale": "ING"},
        back.Banque.BARCLAYS: {
            "id_organisme_preteur": "99999",
            "raison_sociale": "Barclays",
        },
        back.Banque.CREDIT_FONCIER: {
            "id_organisme_preteur": "43199",
            "raison_sociale": "CREDIT FONCIER DE FRANCE",
        },
        back.Banque.AUTRE: {
            "id_organisme_preteur": "99999",
            "raison_sociale": "Autre / je ne sais pas",
        },
    }
    return mapping[b]


def compute_garantie(assure: Assure, simulation: Simulation) -> PackageGaranties:
    if assure.profession == Profession.RETRAITE:
        return PackageGaranties.DC
    if simulation.objet_pret == ObjetPret.INVESTISSEMENT_LOCATIF:
        return PackageGaranties.DC
    if simulation.objet_pret in [
        ObjetPret.RESIDENCE_PRINCIPALE,
        ObjetPret.RESIDENCE_SECONDAIRE,
    ]:
        return PackageGaranties.DC_IPT_IPP_MNO
    return PackageGaranties.DC_IPT_MNO


def to_zenioo_api(simulation_input: Simulation, code_produit):
    beneficiares, garanties, prets = [], [], []
    numero_assure, numero_pret = 1, 1
    contrat = get_contrat(simulation_input.objet_pret, simulation_input.objet_demande)
    simulation = get_simulation("123", code_produit)
    # simulation = get_simulation(data.id, code_produit)
    for pret in simulation_input.prets:
        prets += [get_pret(pret, numero_pret)]
        numero_pret += 1
    for assure in simulation_input.assures:
        beneficiares += [
            get_beneficiare(
                assure, int(simulation_input.prets[0].montant), numero_assure
            )
        ]
        garantie = (
            PackageGaranties.to_zenioo(simulation_input.garantie)
            if simulation_input.garantie is not None
            else compute_garantie(
                assure,
                simulation_input,
            )
        )
        garanties += [get_garantie(numero_assure, assure.quotite, garantie)]
        numero_assure += 1
    return contrat, beneficiares, simulation, prets, garanties


def get_garantie(
    rang_beneficiaire: int,
    quotite: int,
    package_garanties: PackageGaranties,
    franchise: int = 90,
):
    return {
        "rang_beneficiaire": rang_beneficiaire,
        "quotite": quotite,
        "package_garanties": package_garanties.value,
        "franchise": franchise,
    }


def get_pret(pret: Pret, numero: int):
    return {
        "rang_pret": numero,
        "crd": pret.montant,
        "type_pret": {
            TypePret.AMORTISSABLE: "amortissable",
            TypePret.IN_FINE: "in_fine",
            TypePret.PRET_RELAIS: "relais",
            TypePret.PRET_TAUX_ZERO: "relais",
        }[pret.type_pret],
        "taux_pret": pret.taux,
        "duree_remboursement_mois": pret.duree,
        "dont_differe_mois": pret.differe,
    }


def get_simulation(id: str, code_produit: str):
    return {
        "id_projet_partenaire": id,
        "code_produit": code_produit,
        "taux_commission": "40/10",
    }


def get_contrat(objet_pret: ObjetPret, objet_financement: ObjetDemande):
    return {
        "type_projet": objet_pret.value,
        "type_contrat": "resiliation_delegation"
        if objet_financement == ObjetDemande.CHANGEMENT_ASSURANCE
        else "nouveau_pret",
        "date_effet": _to_zenioo_date(
            (datetime.datetime.today() + datetime.timedelta(days=60)).date()
        ),
        "periodicite": "mensuel",
    }


def get_beneficiare(assure: Assure, capital: int, numero: int):
    return {
        "rang_beneficiaire": numero,
        "role": "souscripteur" if numero == 1 else "co_assure",
        "type_assure": "emprunteur",
        "civilite": "monsieur" if assure.genre == Genre.HOMME else "madame",
        "nom": faker.last_name() if assure.nom is None else assure.nom,
        "prenom": faker.first_name() if assure.prenom is None else assure.prenom,
        "date_naissance": _to_zenioo_date(assure.date_naissance),
        "risque_km_pro": "aucun"
        if assure.deplacements_pro == DeplacementsPro.AUCUN
        else (
            "inf_20000"
            if assure.deplacements_pro == DeplacementsPro.MOINS_20000
            else "sup_20000"
        ),
        "risque_travail_manuel": {
            TravauxManuels.AUCUN: "aucun",
            TravauxManuels.LEGERS: "sans_outils",
            TravauxManuels.IMPORTANTS: "avec_outils",
        }[assure.travaux_manuels],
        "risque_fumeur": "fumeur" if assure.fumeur else "non_fumeur",
        "statut_professionnel": {
            Profession.AGRICULTEUR: "agriculteur",
            Profession.ARTISAN: "artisan",
            Profession.AU_FOYER: "sans_emploi",
            Profession.CHEF_ENTREPRISE: "entrepreneur",
            Profession.COMMERCANT: "commercant",
            Profession.EMPLOYE_BUREAU: "employe_bureau",
            Profession.EMPLOYE_BUREAU: "employe_bureau",
            Profession.ENSEIGNANT: "salarie",
            Profession.ETUDIANT: "sans_emploi",
            Profession.FONCTIONNAIRE: "salarie",
            Profession.FORAIN: "liberal",
            Profession.INTERMITTENT: "intermittent",
            Profession.MEDECIN_SPECIALISTE: "medical_liberal",
            Profession.PARAMEDICAL_LIBERAL: "paramedical_liberal",
            Profession.PROFESSION_LIBERALE: "liberal",
            Profession.RECHERCHE_EMPLOI: "sans_emploi",
            Profession.RETRAITE: "retraite",
            Profession.SALARIE_CADRE: "cadre_classe_a",
            Profession.SALARIE_NON_CADRE: "salarie",
            Profession.SANS_ACTIVITE: "sans_emploi",
            Profession.VETERINAIRE: "paramedical_liberal",
            Profession.VRP: "salarie",
        }[assure.profession],
        "email": assure.email,
        "mobile": assure.telephone,
        "code_postal": faker.postcode()
        if assure.code_postal is None
        else assure.code_postal,
        "encours_inf_200000": "inf_200000" if capital < 200000 else "sup_200000",
        "frais_courtage": 70,
        "ville": assure.ville,
        "adresse1": assure.adresse,
        "profession": assure.profession.value,
    }
