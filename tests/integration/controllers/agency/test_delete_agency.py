import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_agencies(db):
    from src.schemas.agency import AgencyIn
    from src.services.agency import AgencyService

    service = AgencyService()
    await service.create(AgencyIn(name="Agency 1",
                                  address="Boulevard Street 13"))
    await service.create(AgencyIn(name="Agency 2",
                                  address="Boulevard Street 13"))
    await service.create(AgencyIn(name="Agency 3",
                                  address="Boulevard Street 13"))


async def test_delete_agency_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    agency_id = 2

    # When
    response = await client.delete(f"/agencies/{agency_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_agency_not_authenticated(client: AsyncClient):
    # Given
    agency_id = 2

    # When
    response = await client.delete(f"/agencies/{agency_id}", headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_agency_not_found(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    agency_id = 99

    # When
    response = await client.delete(f"/agencies/{agency_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_agency_profile_client(client: AsyncClient,
                                            access_client: str):
    # Given
    headers = {"Authorization": f"Bearer {access_client}"}
    agency_id = 2

    # When
    response = await client.delete(f"/agencies/{agency_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
