import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "exames"
exames = sa.Table(
    "exames",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("atendimento_id", sa.Integer, sa.ForeignKey("atendimento.id"),
              nullable=False),
    sa.Column("nome_exame", sa.String(120), nullable=False),
    sa.Column("resultado", sa.String(500), default="Aguardar resultado",
              nullable=False),
    sa.Column("valor_exame", sa.Float, nullable=False),
    sa.Column("status", sa.String(30), default="Solicitado", nullable=False),
)
