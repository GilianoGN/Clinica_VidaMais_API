from pydantic import BaseModel  # type: ignore
from datetime import datetime


# Definição de modelo de entrada para criação de atendimento
class AtendiIn(BaseModel):
    agenda_id: int
    data_atendi: datetime
    evolucao_clinica: str
    diagnostico: str


# Definição de modelo de entrada para atualização do atendimento
class AtendiUpdateIn(BaseModel):
    agenda_id: int | None = None
    data_atendi: datetime | None = None
    evolucao_clinica: str | None = None
    diagnostico: str | None = None
