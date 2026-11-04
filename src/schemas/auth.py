from pydantic import BaseModel  # type: ignore


# Definição de modelo de entrada para login
class LoginIn(BaseModel):
    username: str
    password: str
