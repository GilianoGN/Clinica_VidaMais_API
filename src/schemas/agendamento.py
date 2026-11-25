from enum import Enum
from pydantic import BaseModel  # type: ignore


# Definição do Enum para tipos de perfil de usuário
class TipoAtendimento(str, Enum):
    NORM = "Normal"
    EMER = "Emergencia"


class StatusAgendamento(str, Enum):
    AGEN = "Agendada"
    CONF = "Confirmada"
    CANC = "Cancelada"
    REAL = "Realizada"


# Definição de modelo de entrada para criação de usuário
class AgendamentoIn(BaseModel):
    dataHora: str
    tipoAntendimento: TipoAtendimento = TipoAtendimento.NORM
    status: StatusAgendamento = StatusAgendamento.AGEN
    valorConsulta: float
    pago: bool


# Definição de modelo de entrada para atualização de usuário
class UserUpdateIn(BaseModel):
    name: str | None = None
    document: str | None = None
    profile: ProfileEnum | None = None
    password: str | None = None
