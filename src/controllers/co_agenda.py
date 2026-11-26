from fastapi import status, APIRouter, Depends  # type: ignore
from schemas.sc_agenda import AgendaIn, AgendaUpdateIn
from views.vi_agenda import AgendasListOut
from services.se_agenda import AgendaService
from src.security import get_current_admin_user


router = APIRouter(prefix="/agendas")


service = AgendaService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=AgendasListOut)
async def agendar(agenda: AgendaIn, admin=Depends(get_current_admin_user)):
    return {**agenda.model_dump(), "id": await service.create(agenda)}


@router.get("/", response_model=list[AgendasListOut])
async def list_agendas(limit: int, skip: int = 0,
                       admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=AgendasListOut)
async def read_agenda(id: int, admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=AgendasListOut)
async def update_agenda(id: int, agenda: AgendaUpdateIn,
                        admin=Depends(get_current_admin_user)):
    return await service.update(id=id, agenda=agenda)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_agenda(id: int, admin=Depends(get_current_admin_user)):
    await service.delete(id)
