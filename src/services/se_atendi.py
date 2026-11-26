from database.interfaces import Record  # type: ignore
from src.exceptions import NotFoundAtendiError
from src.database import database
from models.mo_atendi import atendis
from schemas.sc_atendi import AtendiIn, AtendiUpdateIn


class AtendiService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = atendis.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, atendi: AtendiIn) -> int:
        # Verifica se já existe um atendimento com o mesmo nome
        existing_atendi = await self.get_by_nome(atendi.nome)
        if existing_atendi:
            from fastapi import HTTPException, status  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Atendimento with this name already exists."
            )
        command = atendis.insert().values(
            nome=atendi.nome,
            crm=atendi.crm,
            especialidade=atendi.especialidade,
            disponivel=atendi.disponivel,
        )
        return await database.execute(command)

    async def update(self, id: int, atendi: AtendiUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = atendi.model_dump(exclude_unset=True)
        command = atendis.update().where(atendis.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def __get_by_id(self, id) -> Record:
        query = atendis.select().where(atendis.c.id == id)
        atendi = await database.fetch_one(query)
        if not atendi:
            raise NotFoundAtendiError
        return atendi

    async def get_by_nome(self, nome: str) -> Record | None:
        query = atendis.select().where(atendis.c.nome == nome)
        atendi = await database.fetch_one(query)
        if not atendi:
            raise NotFoundAtendiError
        return atendi
