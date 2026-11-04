from databases.interfaces import Record  # type: ignore
from src.exceptions import NotFoundAgencyError
from src.database import database
from src.models.agency import agencies
from src.schemas.agency import AgencyIn, AgencyUpdateIn


class AgencyService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = agencies.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, agency: AgencyIn) -> int:
        # Verifica se já existe uma agencia com o mesmo nome
        existing_agency = await self.get_by_name(agency.name)
        if existing_agency:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Agency with this name already exists."
            )
        command = agencies.insert().values(
            name=agency.name,
            address=agency.address,
        )
        return await database.execute(command)

    async def update(self, id: int, agency: AgencyUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = agency.model_dump(exclude_unset=True)
        command = agencies.update().where(agencies.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.__get_by_id(id)
        command = agencies.delete().where(agencies.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = agencies.select().where(agencies.c.id == id)
        agency = await database.fetch_one(query)
        if not agency:
            raise NotFoundAgencyError
        return agency

    async def get_by_name(self, name: str) -> Record | None:
        query = agencies.select().where(agencies.c.name == name)
        return await database.fetch_one(query)
