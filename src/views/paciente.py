from pydantic import BaseModel  # type: ignore


# Definição de modelo de saída para lista de médicos
class PacientesListOut(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: str


# Definica de modelo de saída para verificação de disponibilidade
class PacientePagamentoOut(BaseModel):
    id: int
    nome: str
    pagamento_em_dia: bool
