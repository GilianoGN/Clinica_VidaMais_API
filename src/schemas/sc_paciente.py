from pydantic import BaseModel  # type: ignore


# Definição de modelo de entrada para criação de paciente
class PacienteIn(BaseModel):
    nome: str
    cpf: str
    idade: int
    telefone: str
    documento_em_dia: bool = True
    pagamento_em_dia: bool = True


# Definição de modelo de entrada para atualização de paciente
class PacienteUpdateIn(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    idade: int | None = None
    telefone: str | None = None
    documento_em_dia: bool | None = None
    pagamento_em_dia: bool | None = None
