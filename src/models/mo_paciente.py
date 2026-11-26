import sqlalchemy as sa  # type: ignore
from src.database import metadata


# Definição do modelo de dados para a tabela "pacientes"
pacientes = sa.Table(
    "pacientes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("nome", sa.String(120), nullable=False),
    sa.Column("cpf", sa.String(14), nullable=False, unique=True),
    sa.Column("idade", sa.Integer, nullable=False),
    sa.Column("telefone", sa.String(20), nullable=False),
    sa.Column("documentos_em_dia", sa.Boolean, default=True, nullable=False),
    sa.Column("pagamento_em_dia", sa.Boolean, default=True, nullable=False),
)
