import sqlalchemy as sa  # type: ignore
from src.database import metadata
from datetime import datetime

# Definição do modelo de dados para a tabela "agendamentos"
agendamentos = sa.Table(
    "agendamentos",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("paciente_id", sa.Integer, sa.ForeignKey("paciente.id"),
              nullable=False),
    sa.Column("medico_id", sa.Integer, sa.ForeignKey("medico.id"),
              nullable=False),
    sa.Column("data_hora", sa.DateTime, default=datetime.now, nullable=True),
    sa.Column("tipo_atendimento", sa.String(10), nullable=False,
              default="Normal"),
    sa.Column("status", sa.String(10), nullable=False, default="Agendada"),
    sa.Column("valor_consulta", sa.Float, nullable=False, default=0.0),
    sa.Column("pago", sa.Boolean, nullable=False, default=False),
)
