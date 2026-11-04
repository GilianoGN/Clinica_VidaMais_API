from enum import Enum
from pydantic import BaseModel  # type: ignore


# Definição do Enum para tipos de perfil de usuário
class ProfileEnum(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"


# Definição de modelo de entrada para criação de usuário
class UserIn(BaseModel):
    name: str
    document: str
    profile: ProfileEnum = ProfileEnum.CLIENT
    password: str


# Definição de modelo de entrada para atualização de usuário
class UserUpdateIn(BaseModel):
    name: str | None = None
    document: str | None = None
    profile: ProfileEnum | None = None
    password: str | None = None
