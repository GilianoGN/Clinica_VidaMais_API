from pydantic import BaseModel, AwareDatetime, NaiveDatetime  # type: ignore
from src.schemas.transaction import TransactionTypeEnum, StatementTypeEnum


# Definição de modelo de saída para lista de transações
class TransactionsListOut(BaseModel):
    id: int
    account_id: int
    destination_account_id: int | None
    type: TransactionTypeEnum
    statement_type: StatementTypeEnum
    amount: float
    timestamp: AwareDatetime | NaiveDatetime | None
