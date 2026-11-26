import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_users(db):
    from schemas.sc_user import UserIn
    from services.se_user import UserService

    service = UserService()
    await service.create(UserIn(name="user 1",
                                document="11111111111",
                                profile="client",
                                password="123456"))
    await service.create(UserIn(name="user 2",
                                document="22222222222",
                                profile="admin",
                                password="123456"))
    await service.create(UserIn(name="user 3",
                                document="33333333333",
                                profile="client",
                                password="123456"))


async def test_list_users_success(client: AsyncClient, access_admin: str):
    # Given
    params = {"limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/users/", params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 5


async def test_list_users_not_authenticated(client: AsyncClient):
    # Given
    params = {"limit": 10, "skip": 0}

    # When
    response = await client.get("/users/", params=params)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_list_users_empty_parameters(client: AsyncClient,
                                           access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/users/", params={}, headers=headers)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_list_users_profile_client(client: AsyncClient,
                                         access_client: str):
    # Given
    params = {"limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_client}"}

    # When
    response = await client.get("/users/", params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
