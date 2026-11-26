import sqlalchemy as sa  # type: ignore
from src.database import metadata
from datetime import datetime


# Definição do modelo de dados para a tabela "atendimentos"
atendis = sa.Table(
    "atendis",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("agenda_id", sa.Integer, sa.ForeignKey("agenda.id"),
              nullable=False),
    sa.Column("data_atendi", sa.DateTipe, default=datetime.now,
              nullable=False),
    sa.Column("evolucao_clinica", sa.String(1000), nullable=False),
    sa.Column("diagnostico", sa.String(500), nullable=False),
)
