from pydantic import BaseModel  # type: ignore


# Definição de modelo de entrada para criação de medico
class MedicoIn(BaseModel):
    nome: str
    crm: str
    especialidade: str
    disponivel: bool = False


# Definição de modelo de entrada para atualização de medico
class MedicoUpdateIn(BaseModel):
    nome: str | None = None
    crm: str | None = None
    especialidade: str | None = None
    disponivel: bool | None = None
