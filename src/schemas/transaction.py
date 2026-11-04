from enum import Enum
from pydantic import BaseModel, Field  # type: ignore


# Definição de Enum para tipos de transação
class TransactionTypeEnum(str, Enum):
    DEPOSIT = "deposito"
    WITHDRAW = "saque"
    TRANSFER = "transferencia"


class StatementTypeEnum(str, Enum):
    ALL = "all"
    DEBIT = "debit"
    CREDIT = "credit"


# Definição de modelo de entrada para criação de transação
class TransactionIn(BaseModel):
    account_id: int
    destination_account_id: int | None = None
    type: TransactionTypeEnum
    statement_type: StatementTypeEnum
    amount: float = Field(gt=0, description="O valor deve ser maior que zero")
