from pydantic import BaseModel


class Result(BaseModel):
    tarif: float = 0.0
    compagnie: str = ""
    nom: str = ""
    garantie: str = ""
    id_tarif: str = ""
    url: str = ""
