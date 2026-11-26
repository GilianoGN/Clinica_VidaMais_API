from controllers import co_agenda, co_atendi, co_exame, co_medico
from fastapi import FastAPI, status, Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from controllers import co_auth, co_paciente, co_user
from src.controllers import receita
from src.exceptions import NotFoundMedicoError, NotFoundUserError
from src.exceptions import NotFoundAgendaError, NotFoundExameError
from src.exceptions import NotFoundPacienteError, NotFoundAtendiError
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
        "name": "medicos",
        "description": "Manutenção do cadastro de **Médicos**. Acesso restrito a Admins.",
    },
    {
        "name": "pacientes",
        "description": "Manutenção do cadastro de **Paciente**. Acesso restrito a Recepção.",
    },
    {
        "name": "agendamentos",
        "description": "Operações de **Agendamento de Consulta**. Acesso restrito a Recepção.",
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


app.include_router(co_auth.router, tags=["auth"])
app.include_router(co_agenda.router, tags=["agendas"])
app.include_router(co_atendi.router, tags=["atendimentos"])
app.include_router(co_exame.router, tags=["exames"])
app.include_router(co_medico.router, tags=["medicos"])
app.include_router(co_paciente.router, tags=["pacientes"])
app.include_router(receita.router, tags=["receitas"])
app.include_router(co_user.router, tags=["users"])


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


@app.exception_handler(NotFoundAgendaError)
async def not_found_agend_exception_handler(request: Request,
                                            exc: NotFoundAgendamentoError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Agendamento not found!"},
    )


@app.exception_handler(NotFoundAtendiError)
async def not_found_atend_exception_handler(request: Request,
                                            exc: NotFoundAtendiError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Atendimento not found!"},
    )


@app.exception_handler(NotFoundPacienteError)
async def not_found_paciente_exception_handler(request: Request,
                                               exc: NotFoundPacienteError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Paciente not found!"},
    )


@app.exception_handler(NotFoundExameError)
async def not_found_exame_exception_handler(request: Request,
                                            exc: NotFoundExameError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Exame not found!"},
    )
