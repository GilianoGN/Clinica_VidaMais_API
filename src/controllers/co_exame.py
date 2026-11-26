from fastapi import status, APIRouter, Depends  # type: ignore
from schemas.sc_exame import ExameIn, ExameUpdateIn
from views.vi_exame import ExamesListOut
from services.se_exame import ExameService
from src.security import get_current_admin_user


router = APIRouter(prefix="/exames")


service = ExameService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=ExamesListOut)
async def create_exame(exame: ExameIn,
                       admin=Depends(get_current_admin_user)):
    return {**exame.model_dump(), "id": await service.create(exame)}


@router.get("/", response_model=list[ExamesListOut])
async def list_exames(limit: int, skip: int = 0,
                      admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=ExamesListOut)
async def read_exame(id: int, admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=ExamesListOut)
async def update_exame(id: int, exame: ExameUpdateIn,
                       admin=Depends(get_current_admin_user)):
    return await service.update(id=id, exame=exame)
