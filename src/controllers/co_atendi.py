from fastapi import status, APIRouter, Depends  # type: ignore
from schemas.sc_atendi import AtendiIn, AtendiUpdateIn
from views.vi_atendi import AtendisListOut
from services.se_atendi import AtendiService
from src.security import get_current_admin_user


router = APIRouter(prefix="/atendimentos")


service = AtendiService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=AtendisListOut)
async def create_atendi(atendi: AtendiIn,
                        admin=Depends(get_current_admin_user)):
    return {**atendi.model_dump(), "id": await service.create(atendi)}


@router.get("/", response_model=list[AtendisListOut])
async def list_atendis(limit: int, skip: int = 0,
                       admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=AtendisListOut)
async def read_atendi(id: int, admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=AtendisListOut)
async def update_atendi(id: int, atendi: AtendiUpdateIn,
                        admin=Depends(get_current_admin_user)):
    return await service.update(id=id, atendi=atendi)
