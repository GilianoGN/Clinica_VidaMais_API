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


async def test_list_agency_success(client: AsyncClient, access_admin: str):
    # Given
    params = {"limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/agencies/", params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 3


async def test_list_agency_not_authenticated(client: AsyncClient):
    # Given
    params = {"limit": 10, "skip": 0}

    # When
    response = await client.get("/agencies/", params=params)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_list_agency_empty_parameters(client: AsyncClient,
                                            access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/agencies/", params={}, headers=headers)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_list_agency_profile_client(client: AsyncClient,
                                          access_client: str):
    # Given
    params = {"limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_client}"}

    # When
    response = await client.get("/agencies/", params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
