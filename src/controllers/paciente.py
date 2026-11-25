from fastapi import status, APIRouter, Depends  # type: ignore
from src.schemas.paciente import PacienteIn, PacienteUpdateIn
from src.views.paciente import PacientesListOut
from src.services.paciente import PacienteService
from src.security import get_current_admin_user


router = APIRouter(prefix="/pacientes")


service = PacienteService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=PacientesListOut)
async def create_paciente(paciente: PacienteIn,
                          admin=Depends(get_current_admin_user)):
    return {**paciente.model_dump(), "id": await service.create(paciente)}


@router.get("/", response_model=list[PacientesListOut])
async def list_pacientes(limit: int, skip: int = 0,
                         admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=PacientesListOut)
async def read_paciente(id: int, admin=Depends(get_current_admin_user)):
    return await service.read(id)


@router.patch("/{id}", response_model=PacientesListOut)
async def update_paciente(id: int, paciente: PacienteUpdateIn,
                          admin=Depends(get_current_admin_user)):
    return await service.update(id=id, paciente=paciente)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_paciente(id: int, admin=Depends(get_current_admin_user)):
    await service.delete(id)
