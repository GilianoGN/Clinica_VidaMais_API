import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "transactions"
transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("account_id", sa.Integer,
              sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("destination_account_id", sa.Integer,
              sa.ForeignKey("accounts.id"), nullable=True),
    sa.Column("type", sa.String(20), nullable=False),
    sa.Column("statement_type", sa.String(20), nullable=False),
    sa.Column("amount", sa.Float, nullable=False),
    sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=True),
    )
