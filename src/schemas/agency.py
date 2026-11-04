from pydantic import BaseModel  # type: ignore


# Definição de modelo de entrada para criação de agência
class AgencyIn(BaseModel):
    name: str
    address: str


# Definição de modelo de entrada para atualização de agência
class AgencyUpdateIn(BaseModel):
    name: str | None = None
    address: str | None = None
