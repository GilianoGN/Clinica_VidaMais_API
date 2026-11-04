import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "agencies"
agencies = sa.Table(
    "agencies",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False, unique=True),
    sa.Column("address", sa.String(150), nullable=False),
    )
