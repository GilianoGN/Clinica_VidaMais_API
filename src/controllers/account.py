from fastapi import status, APIRouter, Depends  # type: ignore
from src.schemas.account import AccountIn
from src.views.account import AccountsListOut
from src.services.account import AccountService
from src.security import get_current_user


router = APIRouter(prefix="/accounts")


service = AccountService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=AccountsListOut)
async def create_account(account: AccountIn,
                         user=Depends(get_current_user)):
    user_id = user["user_id"]
    account_id = await service.create(user_id=user_id, account=account)
    return {
        "id": account_id,
        "user_id": user_id,
        "agency_id": account.agency_id,
        "type": account.type,
        "balance": 0.0
    }


@router.get("/", response_model=list[AccountsListOut])
async def list_accounts(limit: int, skip: int = 0,
                        user=Depends(get_current_user)):
    user_id = user["user_id"]
    return await service.read_all(user_id=user_id, limit=limit, skip=skip)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_account(id: int,
                         user=Depends(get_current_user)):
    user_id = user["user_id"]
    await service.delete(user_id=user_id, id=id)
