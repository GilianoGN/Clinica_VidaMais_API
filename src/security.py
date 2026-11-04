import time
from typing import Annotated
from uuid import uuid4

import jwt  # type: ignore
from fastapi import Depends, HTTPException, Request, status  # type: ignore
from fastapi.security import HTTPBearer  # type: ignore
from pydantic import BaseModel  # type: ignore

SECRET = "sua_chave_secreta_super_segura_com_mais_de_32_caracteres_aqui"
ALGORITHM = "HS256"


# class AccessToken(BaseModel):
#    iss: str
#    sub: int
#    aud: str
#    exp: float
#    iat: float
#    nbf: float
#    jti: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


def sign_jwt(user_id: int, profile: str) -> dict:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),
        "profile": profile,
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),  # 30 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


async def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, SECRET,
                                   algorithms=[ALGORITHM],
                                   options={"verify_aud": False})
        if decoded_token.get("exp", 0) < time.time():
            return None
        return decoded_token
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid authentication scheme.")

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid or expired token.")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication code.")


# Dependência para qualquer usuário autenticado
async def get_current_user(
        token: Annotated[dict, Depends(JWTBearer())]
        ) -> dict:
    return {
        "user_id": int(token.get("sub")),
        "profile": token.get("profile")
    }


# Dependência restrita apenas a usuário administrador
async def get_current_admin_user(
        current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    if current_user.get("profile") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrator can perform this action."
        )
    return current_user
