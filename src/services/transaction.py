from databases.interfaces import Record  # type: ignore
from fastapi import HTTPException, status  # type: ignore
from src.database import database
from src.models.account import accounts
from src.models.transaction import transactions
from src.schemas.transaction import (
    TransactionIn, TransactionTypeEnum, StatementTypeEnum,
)


class TransactionService:
    async def get_statement(self, account_id: int,
                            statement_type: StatementTypeEnum, limit: int,
                            skip: int = 0) -> list[Record]:

        # Busca transações onde a conta é origem ou destino.
        query = transactions.select().where(
            (transactions.c.account_id == account_id) |
            (transactions.c.destination_account_id == account_id)
        )

        # Filtra transações Débito se for origem.
        if statement_type == StatementTypeEnum.DEBIT:
            query = query.where(
                (transactions.c.account_id == account_id) &
                (transactions.c.statement_type == StatementTypeEnum.DEBIT)
            )

        # Filtra transações Crédito se for origem ou Debito se for destino
        elif statement_type == StatementTypeEnum.CREDIT:
            query = query.where(
                ((transactions.c.statement_type == StatementTypeEnum.CREDIT) &
                 (transactions.c.account_id == account_id)) |
                (transactions.c.destination_account_id == account_id)
            )
        query = query.limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create_deposit(self, transaction: TransactionIn) -> int:
        if transaction.type != TransactionTypeEnum.DEPOSIT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid transaction type for deposit."
            )

        # Buscar a conta para atualizar o saldo
        account_query = accounts.select().where(
            accounts.c.id == transaction.account_id)
        account = await database.fetch_one(account_query)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )

        # Executar inserção e atualização em bloco transacional
        async with database.transaction():

            # Atualizar o saldo da conta
            new_balance = account.balance + transaction.amount
            update_cmd = accounts.update().where(
                accounts.c.id == transaction.account_id
            ).values(balance=new_balance)
            await database.execute(update_cmd)

            # Registrar a transação
            insert_cmd = transactions.insert().values(
                account_id=transaction.account_id,
                destination_account_id=None,
                type=transaction.type,
                statement_type=StatementTypeEnum.CREDIT,
                amount=transaction.amount,
            )
            transaction_id = await database.execute(insert_cmd)
        return transaction_id

    async def create_withdrawal(self, transaction: TransactionIn) -> int:
        if transaction.type != TransactionTypeEnum.WITHDRAW:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid transaction type for withdrawal."
            )

        # Buscar a conta para atualizar o saldo
        account_query = accounts.select().where(
            accounts.c.id == transaction.account_id
        )
        account = await database.fetch_one(account_query)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )

        # Validar se há saldo suficiente para o saque
        if account.balance < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance for withdrawal."
            )

        # Executar inserção e atualização em bloco transacional
        async with database.transaction():

            # Atualizar o saldo da conta
            new_balance = account.balance - transaction.amount
            update_cmd = accounts.update().where(
                accounts.c.id == transaction.account_id
            ).values(balance=new_balance)
            await database.execute(update_cmd)

            # Registrar a transação
            insert_cmd = transactions.insert().values(
                account_id=transaction.account_id,
                type=transaction.type,
                statement_type=StatementTypeEnum.DEBIT,
                amount=transaction.amount,
            )
            transaction_id = await database.execute(insert_cmd)
        return transaction_id

    async def create_transfer(self, transaction: TransactionIn) -> int:
        if transaction.type != TransactionTypeEnum.TRANSFER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid transaction type for transfer."
            )
        if not transaction.destination_account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Destination account ID is required for transfer."
            )

        # Buscar a conta de origem para atualizar o saldo
        source_account = await database.fetch_one(
            accounts.select().where(accounts.c.id == transaction.account_id)
        )

        # Buscar a conta de destino para atualizar o saldo
        destin_account = await database.fetch_one(
            accounts.select().where(
                accounts.c.id == transaction.destination_account_id
            )
        )

        # Validar se as contas de origem e destino existem
        if not source_account or not destin_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source or destination account not found."
            )

        # Verificar se as contas de origem e destino são diferentes
        if source_account.id == destin_account.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and destination accounts must be different."
            )

        # Validar se há saldo suficiente para a transferência
        if source_account.balance < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance for transfer."
            )

        # Executar inserção e atualização em bloco transacional
        async with database.transaction():

            # Debitar na origem e Creditar no destino
            await database.execute(
                accounts.update().where(
                    accounts.c.id == source_account.id).values(
                        balance=source_account.balance - transaction.amount)
            )
            await database.execute(
                accounts.update().where(
                    accounts.c.id == destin_account.id).values(
                        balance=destin_account.balance + transaction.amount)
            )

            # Registrar a transação
            insert_cmd = transactions.insert().values(
                account_id=transaction.account_id,
                destination_account_id=transaction.destination_account_id,
                type=transaction.type,
                statement_type=StatementTypeEnum.DEBIT,
                amount=transaction.amount,
            )
            transaction_id = await database.execute(insert_cmd)
        return transaction_id
