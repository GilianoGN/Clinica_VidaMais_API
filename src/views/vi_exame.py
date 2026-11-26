from pydantic import BaseModel  # type: ignore


# Definição de modelo de saída para lista de exames
class ExamesListOut(BaseModel):
    id: int
    atendi_id: int
    nome_exame: str
    resultado: str
    valor_exame: float
    status: str
