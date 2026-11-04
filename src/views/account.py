from pydantic import BaseModel  # type: ignore
from src.schemas.account import AccountTypeEnum


# Definição de modelo de saída para lista de contas
class AccountsListOut(BaseModel):
    id: int
    user_id: int
    agency_id: int
    type: AccountTypeEnum
    balance: float
