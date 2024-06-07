import datetime
from enum import Enum

import factory
import faker
from pydantic import BaseModel, EmailStr, Field

faker = faker.Faker()


class Genre(Enum):
    FEMME = "F"
    HOMME = "H"
    NON_SPECIFIE = "non_specifie"


class GenreFactory(factory.Factory):
    class Meta:
        model = Genre

    value = factory.Faker("enum", enum_cls=Genre)


class Profession(Enum):
    AGRICULTEUR = "agriculteur"
    ARTISAN = "artisan"
    AU_FOYER = "au_foyer"
    COMMERCANT = "commercant"
    CHEF_ENTREPRISE = "chef_entreprise"
    EMPLOYE_BUREAU = "employe_bureau"
    ENSEIGNANT = "enseignant"
    ETUDIANT = "etudiant"
    FONCTIONNAIRE = "fonctionnaire"
    FORAIN = "forain"
    INTERMITTENT = "intermittent"
    MEDECIN_SPECIALISTE = "medecin_specialiste"
    PARAMEDICAL_LIBERAL = "paramedical_liberal"
    PROFESSION_LIBERALE = "profession_liberale"
    RECHERCHE_EMPLOI = "recherche_emploi"
    RETRAITE = "retraite"
    SALARIE_CADRE = "salarie_cadre"
    SALARIE_NON_CADRE = "salarie_non_cadre"
    SANS_ACTIVITE = "sans_activite"
    VETERINAIRE = "veterinaire"
    VRP = "vrp"


class ProfessionFactory(factory.Factory):
    class Meta:
        model = Profession

    value = factory.Faker("enum", enum_cls=Profession)


class TypePret(Enum):
    AMORTISSABLE = "pret_classique"
    IN_FINE = "in_fine"
    PRET_RELAIS = "pret_relais"
    PRET_TAUX_ZERO = "pret_taux_zero"


class TypePretFactory(factory.Factory):
    class Meta:
        model = TypePret

    value = factory.Faker("enum", enum_cls=TypePret)


class Pret(BaseModel):
    montant: int = Field(
        examples=[134023],
        gt=10000,
    )
    type_pret: TypePret
    taux: float = Field(examples=[2.32], gt=0)
    taux_variable: bool
    duree: int = Field(examples=[231], gt=0, le=300)
    differe: int = Field(examples=[0], ge=0, le=300)
    premiere_mensualite: datetime.date = Field(examples=["2012-04-10"])


class PretFactory(factory.Factory):
    class Meta:
        model = Pret

    type_pret = factory.SubFactory(TypePretFactory)
    montant = factory.Faker("random_int", min=10000, max=1000000)
    taux = factory.Faker("pyfloat", min_value=1, max_value=10, right_digits=2)
    taux_variable = factory.Faker("boolean")
    duree = factory.Faker("random_int", min=1, max=300)
    differe = factory.LazyAttribute(lambda o: faker.random_int(min=0, max=o.duree))
    premiere_mensualite = factory.Faker(
        "date_between",
        start_date=datetime.date(1995, 1, 1),
        end_date=datetime.date(2024, 1, 1),
    )


class DeplacementsPro(Enum):
    AUCUN = "aucun"
    MOINS_20000 = "moins_20000"
    PLUS_20000 = "plus_20000"


class DeplacementsProFactory(factory.Factory):
    class Meta:
        model = DeplacementsPro

    value = factory.Faker("enum", enum_cls=DeplacementsPro)


class TravauxManuels(Enum):
    AUCUN = "aucun"
    LEGERS = "legers"
    IMPORTANTS = "importants"


class TravauxManuelsFactory(factory.Factory):
    class Meta:
        model = TravauxManuels

    value = factory.Faker("enum", enum_cls=TravauxManuels)


class Assure(BaseModel):
    genre: Genre
    date_naissance: datetime.date = Field(examples=["1992-01-03"])
    profession: Profession
    deplacements_pro: DeplacementsPro
    travaux_manuels: TravauxManuels
    fumeur: bool
    quotite: int = Field(examples=[100], ge=10, le=100)
    nom: str | None = Field(default=None, examples=["Pierre"])
    prenom: str | None = Field(default=None, examples=["Dupuis"])
    adresse: str | None = Field(default=None, examples=["17 Rue des Accacias"])
    code_postal: str | None = Field(
        default=None, examples=["75001"], pattern="\\d\\d\\d\\d\\d"
    )
    ville: str | None = Field(default=None, examples=["Paris"])
    telephone: str | None = Field(default=None, examples=["0692148234"])
    email: EmailStr | None = Field(default=None, examples=["pierre.dupuis@gmail.com"])


class AssureFactory(factory.Factory):
    class Meta:
        model = Assure

    genre = factory.SubFactory(GenreFactory)
    date_naissance = factory.Faker("date_of_birth", minimum_age=18)
    profession = factory.SubFactory(ProfessionFactory)
    deplacements_pro = factory.SubFactory(DeplacementsProFactory)
    travaux_manuels = factory.SubFactory(TravauxManuelsFactory)
    fumeur = factory.Faker("boolean")
    quotite = factory.Faker("random_int", min=10, max=100)


class Banque(Enum):
    CREDIT_AGRICOLE = "credit_agricole"
    CAISSE_EPARGNE = "caisse_epargne"
    SOCIETE_GENERALE = "societe_generale"
    BNP = "bnp"
    CREDIT_MUTUEL = "credit_mutuel"
    LCL = "lcl"
    BANQUE_POPULAIRE = "banque_populaire"
    LA_BANQUE_POSTALE = "la_banque_postale"
    CIC = "cic"
    CREDIT_DU_NORD = "credit_du_nord"
    AXA = "axa"
    BRED = "bred"
    FORTUNEO = "fortuneo"
    BOURSORAMA = "boursorama"
    HELLOBANK = "hellobank"
    GROUPAMA = "groupama"
    HSBC = "hsbc"
    ING = "ing"
    BARCLAYS = "barclays"
    CREDIT_FONCIER = "credit_foncier"
    AUTRE = "autre"


class BanqueFactory(factory.Factory):
    class Meta:
        model = Banque

    value = factory.Faker("enum", enum_cls=Banque)


class ObjetPret(Enum):
    RESIDENCE_PRINCIPALE = "residence_principale"
    RESIDENCE_SECONDAIRE = "residence_secondaire"
    INVESTISSEMENT_LOCATIF = "investissement_locatif"
    AUTRE = "autre"


class ObjetPretFactory(factory.Factory):
    class Meta:
        model = ObjetPret

    value = factory.Faker("enum", enum_cls=ObjetPret)


class Origin(Enum):
    ASSURLAND = "assurland"
    OMEROS = "omeros"


class OriginFactory(factory.Factory):
    class Meta:
        model = Origin

    value = factory.Faker("enum", enum_cls=Origin)


class ObjetDemande(Enum):
    NOUVEAU_PRET = "nouveau_pret"
    CHANGEMENT_ASSURANCE = "changement_assurance"
    RENEGOCIATION = "renegociation"


class ObjetDemandeFactory(factory.Factory):
    class Meta:
        model = ObjetDemande

    value = factory.Faker("enum", enum_cls=ObjetDemande)


class Garantie(Enum):
    DC_PTIA = "DC_PTIA"
    DC_PTIA_IPT_ITT = "DC_PTIA_IPT_ITT"
    DC_PTIA_IPT_ITT_MNO = "DC_PTIA_IPT_ITT_MNO"
    DC_PTIA_IPT_ITT_IPP = "DC_PTIA_IPT_ITT_IPP"
    DC_PTIA_IPT_ITT_IPP_MNO = "DC_PTIA_IPT_ITT_IPP_MNO"


class GarantieFactory(factory.Factory):
    class Meta:
        model = Garantie

    value = factory.Faker("enum", enum_cls=Garantie)


class Simulation(BaseModel):
    origin: Origin
    objet_pret: ObjetPret
    objet_demande: ObjetDemande
    banque: Banque
    debut_contrat: datetime.date = Field(examples=["2024-11-09"])
    garantie: Garantie | None = Field(default=None, examples=[Garantie.DC_PTIA])
    prets: list["Pret"]
    assures: list["Assure"]


class SimulationFactory(factory.Factory):
    class Meta:
        model = Simulation

    origin = factory.SubFactory(OriginFactory)
    objet_pret = factory.SubFactory(ObjetPretFactory)
    objet_demande = factory.SubFactory(ObjetDemandeFactory)
    banque = factory.SubFactory(BanqueFactory)
    debut_contrat = factory.Faker("date_this_year", after_today=True)
    garantie = factory.SubFactory(GarantieFactory)
    _nb_prets = factory.Faker("random_int", min=1, max=2)
    prets = factory.LazyAttribute(lambda o: [PretFactory() for _ in range(o._nb_prets)])
    _nb_assures = factory.Faker("random_int", min=1, max=2)
    assures = factory.LazyAttribute(
        lambda o: [AssureFactory() for _ in range(o._nb_assures)]
    )


class SimulationWithId(Simulation):
    id: str


class SimulationId(BaseModel):
    id_simulation: str


class SimulationWithTarif(BaseModel):
    simulation: Simulation
    id_tarif: str
