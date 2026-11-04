from fastapi import status, APIRouter, Depends  # type: ignore
from src.schemas.user import UserIn, UserUpdateIn
from src.views.user import UserOut, UserListOut
from src.services.user import UserService
from src.security import get_current_admin_user


router = APIRouter(prefix="/users")


service = UserService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=UserOut)
async def create_user(user: UserIn,
                      admin=Depends(get_current_admin_user)):
    return {**user.model_dump(), "id": await service.create(user)}


@router.get("/", response_model=list[UserListOut])
async def list_users(limit: int, skip: int = 0,
                     admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=UserOut)
async def read_user(id: int,
                    admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=UserOut)
async def update_user(id: int, user: UserUpdateIn,
                      admin=Depends(get_current_admin_user)):
    return await service.update(id=id, user=user)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_user(id: int,
                      admin=Depends(get_current_admin_user)):
    await service.delete(id)
