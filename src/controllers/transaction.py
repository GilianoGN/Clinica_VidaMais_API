from fastapi import status, APIRouter, Depends, HTTPException  # type: ignore
from src.schemas.transaction import TransactionIn, StatementTypeEnum
from src.views.transaction import TransactionsListOut
from src.services.transaction import TransactionService
from src.services.account import AccountService
from src.security import get_current_user


router = APIRouter(prefix="/transactions")

transaction_service = TransactionService()
account_service = AccountService()


@router.post("/deposit", status_code=status.HTTP_201_CREATED)
async def create_deposit(transaction: TransactionIn,
                         user=Depends(get_current_user)):
    # Verifica se a conta destino (account_id) existe.
    try:
        await account_service._AccountService__get_by_id(
            transaction.account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {transaction.account_id} not found."
        )
    transaction_id = await transaction_service.create_deposit(transaction)
    return {"id": transaction_id, **transaction.model_dump()}


@router.post("/withdrawal", status_code=status.HTTP_201_CREATED)
async def create_withdrawal(transaction: TransactionIn,
                            user=Depends(get_current_user)):
    # Verifica se a conta origem (account_id) existe e pertence ao usuário.
    try:
        account = await account_service._AccountService__get_by_id(
            transaction.account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {transaction.account_id} not found."
        )
    if account.user_id != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to withdraw from this account."
        )
    transaction_id = await transaction_service.create_withdrawal(transaction)
    return {"id": transaction_id, **transaction.model_dump()}


@router.post("/transfer", status_code=status.HTTP_201_CREATED)
async def create_transfer(transaction: TransactionIn,
                          user=Depends(get_current_user)):
    # Verifica se a conta origem (account_id) existe e pertence ao usuário.
    try:
        sou_account = await account_service._AccountService__get_by_id(
            transaction.account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source account with ID {
                transaction.account_id} not found."
        )
    if sou_account.user_id != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to transfer from this account."
        )

    # Verifica se a conta destino (destination_account_id) existe.
    if not transaction.destination_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Destination account ID is required for transfer."
        )
    try:
        await account_service._AccountService__get_by_id(
            transaction.destination_account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination account with ID {
                transaction.destination_account_id} not found."
        )

    transaction_id = await transaction_service.create_transfer(transaction)
    return {"id": transaction_id, **transaction.model_dump()}


@router.get("/statement/{account_id}",
            response_model=list[TransactionsListOut])
async def get_statement(account_id: int,
                        statement: StatementTypeEnum = StatementTypeEnum.ALL,
                        user=Depends(get_current_user),
                        limit: int = 10, skip: int = 0):
    # Listar somente movimentação de uma conta que pertença ao usuário logado.
    try:
        account = await account_service._AccountService__get_by_id(
            account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found."
        )
    if account.user_id != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this account."
        )
    return await transaction_service.get_statement(
        account_id=account_id,
        statement_type=statement,
        limit=limit,
        skip=skip
    )
