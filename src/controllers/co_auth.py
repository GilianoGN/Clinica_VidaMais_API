from fastapi import APIRouter, HTTPException, status  # type: ignore
from passlib.context import CryptContext
from schemas.sc_auth import LoginIn
from src.security import sign_jwt
from services.se_user import UserService
from views.vi_auth import LoginOut


router = APIRouter(prefix="/auth")
user_service = UserService()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    # Buscar o usuário pelo username
    user = await user_service.get_by_username(data.username)

    # Validação segura: verificar o usuário e a senha
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retorna o token JWT assinado
    return sign_jwt(user_id=user["id"], profile=user["profile"])
