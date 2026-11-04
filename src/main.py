from fastapi import FastAPI, status, Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from src.controllers import auth, user, agency, account, transaction
from src.exceptions import NotFoundAgencyError, NotFoundUserError
from src.exceptions import NotFoundAccountError, NotFoundTransactionError
from src.database import database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operações de **autenticação**. Emite tokens JWT para acesso rotas protegidas.",
    },
    {
        "name": "users",
        "description": "Gestão de **usuários** e perfis (Administrador e Cliente). Acesso restrito a Admins.",
    },
    {
        "name": "agencies",
        "description": "Manutenção do cadastro de **agências bancárias**. Acesso restrito a Admins.",
    },
    {
        "name": "accounts",
        "description": "Operações de **contas bancárias** (Corrente e Poupança). Permite criação, consulta e encerramento de contas zeradas.",
    },
    {
        "name": "transactions",
        "description": "Operações de **movimentação financeira** (Depósitos, Saques, Transferências e Extratos).",
    },
]


servers = [
    {"url": "http://127.0.0.1:8000",
     "description": "Ambiente de desenvolvimento."},
    {"url": "https://fastapi-ez1r.onrender.com",
     "description": "Ambiente de produção."},
]


app = FastAPI(
    title="DIO Bank FastAPI",
    version="1.0.0",
    summary="API Restful para Gestão de Contas e Transações Bancárias",
    description="""
# 🏦 DIO Bank API

Bem-vindo à documentação oficial da **DIO Bank API**! Esta aplicação foi construída com **FastAPI**, **Clean Architecture**, **SQLAlchemy Core** e **Alembic**.

### 🔑 Recursos Principais:
* **Autenticação Stateless (JWT)** com suporte a RBAC (*Role-Based Access Control* para `admin` e `client`).
* **Regras de Negócio Financeiras**:
  * Limite de apenas **uma conta corrente por cliente**.
  * Encerramento restrito a contas com **saldo zerado**.
  * Execução atômica de transações bancárias (garantia contra inconsistências).
  * Extrato inteligente com filtragem granular por **Débitos**, **Créditos** ou **Histórico Completo**.

---
*Desenvolvido como projeto prático no ecossistema Python.*
""",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    servers=servers,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, tags=["users"])
app.include_router(agency.router, tags=["agencies"])
app.include_router(account.router, tags=["accounts"])
app.include_router(transaction.router, tags=["transactions"])


@app.exception_handler(NotFoundUserError)
async def not_found_user_exception_handler(request: Request,
                                           exc: NotFoundUserError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found!"},
    )


@app.exception_handler(NotFoundAgencyError)
async def not_found_agency_exception_handler(request: Request,
                                             exc: NotFoundAgencyError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Agency not found!"},
    )


@app.exception_handler(NotFoundAccountError)
async def not_found_account_exception_handler(request: Request,
                                              exc: NotFoundAccountError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Account not found!"},
    )


@app.exception_handler(NotFoundTransactionError)
async def not_found_trans_exception_handler(request: Request,
                                            exc: NotFoundTransactionError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Transaction not found!"},
    )
