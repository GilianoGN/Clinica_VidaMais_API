from fastapi import FastAPI, status, Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from src.controllers import auth, user, agency, account, transaction, medico
from src.exceptions import NotFoundMedicoError, NotFoundUserError
from src.exceptions import NotFoundAgendamentoError, NotFoundExameError
from src.exceptions import NotFoundPacienteError, NotFoundReceitaError
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
        "description": "Gestão de **usuários** e perfis (Administrador, Medico e Atendente). Acesso restrito a Admins.",
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
    title="Clínica Vida+ FastAPI",
    version="1.0.0",
    summary="API Restful para Gestão das atividades da Clínica Vida+",
    description="""
# 🏥 Clínica Vida+ API

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
app.include_router(agendamento.router, tags=["agendamentos"])
app.include_router(atendimento.router, tags=["atendimentos"])
app.include_router(exame.router, tags=["exames"])
app.include_router(medico.router, tags=["medicos"])
app.include_router(paciente.router, tags=["pacientes"])
app.include_router(receita.router, tags=["receitas"])
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


@app.exception_handler(NotFoundMedicoError)
async def not_found_medico_exception_handler(request: Request,
                                             exc: NotFoundMedicoError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Medico not found!"},
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
