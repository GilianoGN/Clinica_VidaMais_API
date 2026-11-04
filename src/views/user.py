from pydantic import BaseModel  # type: ignore
from src.schemas.user import ProfileEnum


# Definição de modelo de saída para usuário
class UserOut(BaseModel):
    id: int
    name: str
    document: str
    profile: ProfileEnum


# Definição de modelo de saída para lista de usuários
class UserListOut(BaseModel):
    id: int
    name: str
    profile: ProfileEnum
