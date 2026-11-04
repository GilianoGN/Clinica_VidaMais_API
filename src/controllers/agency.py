from fastapi import status, APIRouter, Depends  # type: ignore
from src.schemas.agency import AgencyIn, AgencyUpdateIn
from src.views.agency import AgenciesListOut
from src.services.agency import AgencyService
from src.security import get_current_admin_user


router = APIRouter(prefix="/agencies")


service = AgencyService()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=AgenciesListOut)
async def create_agency(agency: AgencyIn,
                        admin=Depends(get_current_admin_user)):
    return {**agency.model_dump(), "id": await service.create(agency)}


@router.get("/", response_model=list[AgenciesListOut])
async def list_agencies(limit: int, skip: int = 0,
                        admin=Depends(get_current_admin_user)):
    return await service.read_all(limit=limit, skip=skip)


@router.patch("/{id}", response_model=AgenciesListOut)
async def update_agency(id: int, agency: AgencyUpdateIn,
                        admin=Depends(get_current_admin_user)):
    return await service.update(id=id, agency=agency)


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_agency(id: int,
                        admin=Depends(get_current_admin_user)):
    await service.delete(id)
