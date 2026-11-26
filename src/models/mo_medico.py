import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "medicos"
medicos = sa.Table(
    "medicos",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("nome", sa.String(120), nullable=False),
    sa.Column("crm", sa.String(20), nullable=False, unique=True),
    sa.Column("especialidade", sa.String(80), nullable=False),
    sa.Column("disponivel", sa.Boolean, default=True, nullable=False),
)
