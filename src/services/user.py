from databases.interfaces import Record  # type: ignore
from passlib.context import CryptContext
from src.exceptions import NotFoundUserError
from src.database import database
from src.models.user import users
from src.schemas.user import UserIn, UserUpdateIn


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = users.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, user: UserIn) -> int:
        # Verifica se já existe um usuário com o mesmo document
        existing_user = await self.get_by_document(user.document)
        if existing_user:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this document already exists."
            )
        # Criptografar a senha antes de salvar no banco de dados
        command = users.insert().values(
            name=user.name,
            document=user.document,
            profile=user.profile,
            password=pwd_context.hash(user.password),
        )
        return await database.execute(command)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(self, id: int, user: UserUpdateIn) -> Record:
        await self.__get_by_id(id)
        data = user.model_dump(exclude_unset=True)
        # Criptografar a senha se ela estiver presente no payload
        if "password" in data:
            data["password"] = pwd_context.hash(data["password"])
        command = users.update().where(users.c.id == id).values(**data)
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.__get_by_id(id)
        command = users.delete().where(users.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = users.select().where(users.c.id == id)
        user = await database.fetch_one(query)
        if not user:
            raise NotFoundUserError
        return user

    async def get_by_username(self, username: str) -> Record | None:
        query = users.select().where(users.c.name == username)
        return await database.fetch_one(query)

    async def get_by_document(self, document: str) -> Record | None:
        query = users.select().where(users.c.document == document)
        return await database.fetch_one(query)
