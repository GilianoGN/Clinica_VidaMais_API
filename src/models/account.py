import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "accounts"
accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer,
              sa.ForeignKey("users.id"), nullable=False),
    sa.Column("agency_id", sa.Integer,
              sa.ForeignKey("agencies.id"), nullable=False),
    sa.Column("type", sa.String(20), nullable=False),
    sa.Column("balance", sa.Float, nullable=False, default=0.0),
)
