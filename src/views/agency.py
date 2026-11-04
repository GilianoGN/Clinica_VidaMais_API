from pydantic import BaseModel  # type: ignore


# Definição de modelo de saída para lista de agências
class AgenciesListOut(BaseModel):
    id: int
    name: str
    address: str
