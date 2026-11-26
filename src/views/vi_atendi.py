from pydantic import BaseModel  # type: ignore
from datetime import datetime


# Definição de modelo de saída para lista de atendimentos
class AtendisListOut(BaseModel):
    id: int
    agenda_id: int
    data_atendi: datetime
    evolucao_clinica: str
    diagnostico: str
