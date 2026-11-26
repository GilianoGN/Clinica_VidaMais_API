from database.interfaces import Record  # type: ignore
from src.exceptions import NotFoundAgendaError
from src.database import database
from models.mo_agenda import agendas
from schemas.sc_agenda import AgendaIn, AgendaUpdateIn


class AgendaService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = agendas.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, agenda: AgendaIn) -> int:
        # Verifica se já existe uma agenda com o mesmo nome
        existing_agenda = await self.get_by_nome(agenda.nome)
        if existing_agenda:
            from fastapi import HTTPException, status  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Agenda with this name already exists."
            )
        command = agendas.insert().values(
            data_hora=agenda.data_hora,
            paciente_id=agenda.paciente_id,
            medico_id=agenda.medico_id,
            tipo_atendi=agenda.tipo_atendi,
            status=agenda.status,
            valor_consulta=agenda.valor_consulta,
            pago=agenda.pago,
        )
        return await database.execute(command)

    async def update(self, id: int, agenda: AgendaUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = agenda.model_dump(exclude_unset=True)
        command = agendas.update().where(agendas.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.__get_by_id(id)
        command = agendas.delete().where(agendas.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = agendas.select().where(agendas.c.id == id)
        agenda = await database.fetch_one(query)
        if not agenda:
            raise NotFoundAgendaError
        return agenda

    async def get_by_nome(self, nome: str) -> Record | None:
        query = agendas.select().where(agendas.c.nome == nome)
        agenda = await database.fetch_one(query)
        if not agenda:
            raise NotFoundAgendaError
        return agenda