import datetime
from typing import List

import common.models.simulation
import factory
from pydantic import BaseModel, EmailStr, Field

TypePret = common.models.simulation.TypePret
TypePretFactory = common.models.simulation.TypePretFactory
Pret = common.models.simulation.Pret
PretFactory = common.models.simulation.PretFactory
Genre = common.models.simulation.Genre
GenreFactory = common.models.simulation.GenreFactory
Profession = common.models.simulation.Profession
ProfessionFactory = common.models.simulation.ProfessionFactory
DeplacementsPro = common.models.simulation.DeplacementsPro
DeplacementsProFactory = common.models.simulation.DeplacementsProFactory
ObjetPret = common.models.simulation.ObjetPret
ObjetPretFactory = common.models.simulation.ObjetPretFactory
TravauxManuels = common.models.simulation.TravauxManuels
TravauxManuelsFactory = common.models.simulation.TravauxManuelsFactory
Garantie = common.models.simulation.Garantie
GarantieFactory = common.models.simulation.GarantieFactory


class Assure(BaseModel):
    genre: Genre
    date_naissance: datetime.date = Field(examples=["1992-01-03"])
    profession: Profession
    deplacements_pro: DeplacementsPro
    travaux_manuels: TravauxManuels
    fumeur: bool
    quotite: int = Field(examples=[100], ge=10, le=100)


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


class Simulation(BaseModel):
    objet_pret: ObjetPret
    debut_contrat: datetime.date = Field(examples=["2024-11-09"])
    garantie: Garantie = Field(default=None, examples=[Garantie.DC_PTIA])
    prets: List[Pret] = Field(min_length=1)
    assures: List[Assure] = Field(min_length=1, max_length=2)


class SimulationFactory(factory.Factory):
    class Meta:
        model = Simulation

    objet_pret = factory.SubFactory(ObjetPretFactory)
    debut_contrat = factory.Faker("date_this_year", after_today=True)
    garantie = factory.SubFactory(GarantieFactory)
    _nb_prets = factory.Faker("random_int", min=1, max=2)
    prets = factory.LazyAttribute(lambda o: [PretFactory() for _ in range(o._nb_prets)])
    _nb_assures = factory.Faker("random_int", min=1, max=2)
    assures = factory.LazyAttribute(
        lambda o: [AssureFactory() for _ in range(o._nb_assures)]
    )


class Coordonnees(BaseModel):
    nom: str = Field(examples=["Pierre"])
    prenom: str = Field(examples=["Dupuis"])
    adresse: str = Field(examples=["17 Rue des Accacias"])
    code_postal: str = Field(examples=["75001"], pattern="\\d\\d\\d\\d\\d")
    ville: str = Field(examples=["Paris"])
    telephone: str = Field(examples=["0692148234"])
    email: EmailStr = Field(examples=["pierre.dupuis@gmail.com"])


class CoordonneesFactory(factory.Factory):
    class Meta:
        model = Coordonnees

    nom = factory.Faker("last_name")
    prenom = factory.Faker("first_name")
    adresse = factory.Faker("street_address")
    code_postal = factory.Faker("postcode")
    ville = factory.Faker("city")
    portable = factory.Faker("phone_number")
    email = factory.Faker("ascii_safe_email")


class Adhesion(BaseModel):
    id_simulation: str
    id_formule: str
    coordonnees: Coordonnees
