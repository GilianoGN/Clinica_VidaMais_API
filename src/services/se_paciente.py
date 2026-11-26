from database.interfaces import Record  # type: ignore
from src.exceptions import NotFoundPacienteError
from src.database import database
from models.mo_paciente import pacientes
from schemas.sc_paciente import PacienteIn, PacienteUpdateIn


class PacienteService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = pacientes.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, paciente: PacienteIn) -> int:
        # Verifica se já existe um paciente com o mesmo nome
        existing_paciente = await self.get_by_nome(paciente.nome)
        if existing_paciente:
            from fastapi import HTTPException, status  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Paciente with this name already exists."
            )
        command = pacientes.insert().values(
            nome=paciente.nome,
            cpf=paciente.cpf,
            idade=paciente.idade,
            telefone=paciente.telefone,
            documento_em_dia=paciente.documento_em_dia,
            pagamento_em_dia=paciente.pagamento_em_dia,
        )
        return await database.execute(command)

    async def update(self, id: int, paciente: PacienteUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = paciente.model_dump(exclude_unset=True)
        command = pacientes.update().where(pacientes.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.__get_by_id(id)
        command = pacientes.delete().where(pacientes.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = pacientes.select().where(pacientes.c.id == id)
        paciente = await database.fetch_one(query)
        if not paciente:
            raise NotFoundPacienteError
        return paciente

    async def get_by_nome(self, nome: str) -> Record | None:
        query = pacientes.select().where(pacientes.c.nome == nome)
        paciente = await database.fetch_one(query)
        if not paciente:
            raise NotFoundPacienteError
        return paciente
