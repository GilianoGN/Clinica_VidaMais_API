import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_account(db):
    from src.schemas.agency import AgencyIn
    from src.services.agency import AgencyService

    service = AgencyService()
    await service.create(AgencyIn(name="Agency 1",
                                  address="Boulevard Street 13"))


async def test_create_account_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"agency_id": 1,
            "type": "corrente"}

    # When
    response = await client.post("/accounts/", headers=headers, json=data)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_account_duplicated_type_corrent(client: AsyncClient,
                                                      access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data1 = {"agency_id": 1,
             "type": "corrente"}
    data2 = {"agency_id": 1,
             "type": "corrente"}

    # When
    response1 = await client.post("/accounts/", headers=headers, json=data1)
    response2 = await client.post("/accounts/", headers=headers, json=data2)

    # Then
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_400_BAD_REQUEST


async def test_create_account_invalid_data(client: AsyncClient,
                                           access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"type": "corrente"}

    # When
    response = await client.post("/accounts/", headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_create_account_not_authenticated(client: AsyncClient):
    # Given
    data = {"agency_id": 1,
            "type": "corrente"}

    # When
    response = await client.post("/accounts/", headers={}, json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
