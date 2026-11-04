import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "users"
users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(150), nullable=False),
    sa.Column("document", sa.String(14), nullable=False, unique=True),
    sa.Column("profile", sa.String(20), nullable=False, default="client"),
    sa.Column("password", sa.String, nullable=False),
    )
