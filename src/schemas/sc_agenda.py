from enum import Enum
from pydantic import BaseModel  # type: ignore
from datetime import date


# Definição do Enum para tipos de perfil de usuário
class TipoAtendi(str, Enum):
    NORM = "Normal"
    EMER = "Emergencia"


class StatusAgenda(str, Enum):
    AGEN = "Agendada"
    CONF = "Confirmada"
    CANC = "Cancelada"
    REAL = "Realizada"


# Definição de modelo de entrada para criação de usuário
class AgendaIn(BaseModel):
    data_hora: date
    paciente_id: int
    medico_id: int
    tipo_atendi: TipoAtendi = TipoAtendi.NORM
    status: StatusAgenda = StatusAgenda.AGEN
    valor_consulta: float
    pago: bool


# Definição de modelo de entrada para atualização de usuário
class AgendaUpdateIn(BaseModel):
    data_hora: date | None = None
    paciente_id: int | None = None
    medico_id: int | None = None
    tipo_atendi: TipoAtendi | None = None
    status: StatusAgenda | None = None
    valor_consulta: float | None = None
    pago: bool | None = None
