from fastapi import status, APIRouter, Depends  # type: ignore
from src.schemas.medico import MedicoIn, MedicoUpdateIn
from src.views.medico import MedicosListOut
from src.services.medico import MedicoService
from src.security import get_current_admin_user


router = APIRouter(prefix="/medicos")


service = MedicoService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=MedicosListOut)
async def create_medico(medico: MedicoIn,
                        admin=Depends(get_current_admin_user)):
    return {**medico.model_dump(), "id": await service.create(medico)}


@router.get("/", response_model=list[MedicosListOut])
async def list_medicos(limit: int, skip: int = 0,
                       admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=MedicosListOut)
async def read_medico(id: int, admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=MedicosListOut)
async def update_medico(id: int, medico: MedicoUpdateIn,
                        admin=Depends(get_current_admin_user)):
    return await service.update(id=id, medico=medico)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_medico(id: int,
                        admin=Depends(get_current_admin_user)):
    await service.delete(id)
