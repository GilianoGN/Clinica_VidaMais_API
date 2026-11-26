from pydantic import BaseModel  # type: ignore
from datetime import date
from schemas.sc_agenda import TipoAtendi, StatusAgenda


# Definição de modelo de saída para lista de agendas
class AgendasListOut(BaseModel):
    id: int
    data_hora: date
    paciente_id: int
    medico_id: int
    tipo_atendi: TipoAtendi
    status: StatusAgenda
    valor_consulta: float
    pago: bool
