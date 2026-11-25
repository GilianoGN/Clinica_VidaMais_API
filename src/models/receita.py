import sqlalchemy as sa  # type: ignore
from src.database import metadata
from datetime import date


# Definição do modelo de dados para a tabela "receitas"
receitas = sa.Table(
    "receitas",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("exame_id", sa.Integer, sa.ForeignKey("exame.id"),
              nullable=False),
    sa.Column("medicamentos", sa.String(1000), nullable=False),
    sa.Column("posologia", sa.String(1000), nullable=False),
    sa.Column("data_emissao", sa.DATE, defaults=date.today, nullable=True),
)
