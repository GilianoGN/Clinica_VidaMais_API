from enum import Enum
from pydantic import BaseModel  # type: ignore


# Definição de Enum para tipos de conta
class AccountTypeEnum(str, Enum):
    CORRENTE = "corrente"
    POUPANCA = "poupanca"


# Definição de modelo de entrada para criação de conta
class AccountIn(BaseModel):
    agency_id: int
    type: AccountTypeEnum


# Definição de modelo de entrada para atualização de valores da conta
class AccountUpdateIn(BaseModel):
    balance: float
