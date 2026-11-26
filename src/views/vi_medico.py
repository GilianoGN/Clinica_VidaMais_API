from pydantic import BaseModel  # type: ignore


# Definição de modelo de saída para lista de médicos
class MedicosListOut(BaseModel):
    id: int
    nome: str
    crm: str
    especialidade: str


# Definica de modelo de saída para verificação de disponibilidade
class MedicoDisponivelOut(BaseModel):
    id: int
    nome: str
    disponivel: bool
