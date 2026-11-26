from database.interfaces import Record  # type: ignore
from src.exceptions import NotFoundMedicoError
from src.database import database
from models.mo_medico import medicos
from schemas.sc_medico import MedicoIn, MedicoUpdateIn


class MedicoService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = medicos.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, medico: MedicoIn) -> int:
        # Verifica se já existe um medico com o mesmo nome
        existing_medico = await self.get_by_nome(medico.nome)
        if existing_medico:
            from fastapi import HTTPException, status  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Medico with this name already exists."
            )
        command = medicos.insert().values(
            nome=medico.nome,
            crm=medico.crm,
            especialidade=medico.especialidade,
            disponivel=medico.disponivel,
        )
        return await database.execute(command)

    async def update(self, id: int, medico: MedicoUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = medico.model_dump(exclude_unset=True)
        command = medicos.update().where(medicos.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.__get_by_id(id)
        command = medicos.delete().where(medicos.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = medicos.select().where(medicos.c.id == id)
        medico = await database.fetch_one(query)
        if not medico:
            raise NotFoundMedicoError
        return medico

    async def get_by_nome(self, nome: str) -> Record | None:
        query = medicos.select().where(medicos.c.nome == nome)
        medico = await database.fetch_one(query)
        if not medico:
            raise NotFoundMedicoError
        return medico
