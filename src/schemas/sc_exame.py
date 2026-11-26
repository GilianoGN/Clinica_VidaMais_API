from pydantic import BaseModel  # type: ignore


# Definição de modelo de entrada para criação de exames
class ExameIn(BaseModel):
    atendi_id: int
    nome_exame: str
    resultado: str
    valor_exame: float
    status: str


# Definição de modelo de entrada para atualização de exame
class ExameUpdateIn(BaseModel):
    atendi_id: int | None = None
    nome_exame: str | None = None
    resultado: str | None = None
    valor_exame: float | None = None
    status: str | None = None
