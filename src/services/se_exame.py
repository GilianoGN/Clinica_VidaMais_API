from database.interfaces import Record  # type: ignore
from src.exceptions import NotFoundExameError
from src.database import database
from models.mo_exame import exames
from schemas.sc_exame import ExameIn, ExameUpdateIn


class MedicoService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = exames.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, exame: ExameIn) -> int:
        # Verifica se já existe um exame com o mesmo nome
        existing_exame = await self.get_by_nome(exame.nome)
        if existing_exame:
            from fastapi import HTTPException, status  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Exame with this name already exists."
            )
        command = exames.insert().values(
            atendi_id=exame.atendi_id,
            nome_exame=exame.nome_exame,
            resultado=exame.resultado,
            valor_exame=exame.valor_exame,
            status=exame.status
        )
        return await database.execute(command)

    async def update(self, id: int, exame: ExameUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = exame.model_dump(exclude_unset=True)
        command = exames.update().where(exames.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def __get_by_id(self, id) -> Record:
        query = exames.select().where(exames.c.id == id)
        exame = await database.fetch_one(query)
        if not exame:
            raise NotFoundExameError
        return exame

    async def get_by_nome(self, nome: str) -> Record | None:
        query = exames.select().where(exames.c.nome == nome)
        exame = await database.fetch_one(query)
        if not exame:
            raise NotFoundExameError
        return exame
