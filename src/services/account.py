from databases.interfaces import Record  # type: ignore
from fastapi import HTTPException, status  # type: ignore
from src.exceptions import NotFoundAccountError
from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn, AccountTypeEnum


class AccountService:
    async def read_all(self, user_id: int,
                       limit: int, skip: int = 0) -> list[Record]:
        # Listar somente as contas do usuário logado
        query = accounts.select().where(
            accounts.c.user_id == user_id
            ).limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, user_id: int, account: AccountIn) -> int:
        # Só poderá haver somente uma conta corrente por usuário
        if account.type == AccountTypeEnum.CORRENTE:
            query_check = accounts.select().where(
                (accounts.c.user_id == user_id) &
                (accounts.c.type == AccountTypeEnum.CORRENTE)
            )
            existing_account = await database.fetch_one(query_check)
            if existing_account:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already has a checking account."
                )
        command = accounts.insert().values(
            user_id=user_id,
            agency_id=account.agency_id,
            type=account.type,
            balance=0.0,
        )
        return await database.execute(command)

    async def delete(self, user_id: int, id: int) -> None:
        # Verificar se a conta é realmente do usuário logado
        account = await self.__get_by_id(id)
        if account.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this account."
            )
        # Verificar se a conta está zerada antes de permitir a exclusão
        if account.balance != 0.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account balance must be zero to delete the account."
            )
        command = accounts.delete().where(accounts.c.id == id)
        await database.execute(command)

    async def update(self, user_id: int, account_id: int,
                     balance: float) -> None:
        # Verificar se a conta é realmente do usuário logado
        account = await self.__get_by_id(account_id)
        if account.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this account."
            )
        command = accounts.update().where(
            accounts.c.id == account_id).values(balance=balance)
        await database.execute(command)

    async def __get_by_id(self, id) -> Record:
        query = accounts.select().where(accounts.c.id == id)
        account = await database.fetch_one(query)
        if not account:
            raise NotFoundAccountError
        return account
