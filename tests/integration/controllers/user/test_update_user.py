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


async def test_update_user_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"name": "User 4"}
    user_id = 2

    # Then
    response = await client.patch(f"/users/{user_id}", json=data,
                                  headers=headers)
    content = response.json()

    # When
    assert response.status_code == status.HTTP_200_OK
    assert content["name"] == data["name"]


async def test_update_user_not_authenticated(client: AsyncClient):
    # Given
    data = {"name": "User 4"}
    user_id = 2

    # Then
    response = await client.patch(f"/users/{user_id}", json=data, headers={})

    # When
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_update_user_not_found(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"name": "User 4"}
    user_id = 99

    # Then
    response = await client.patch(f"/users/{user_id}", json=data,
                                  headers=headers)

    # When
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_user_profile_client(client: AsyncClient,
                                          access_client: str):
    # Given
    headers = {"Authorization": f"Bearer {access_client}"}
    data = {"name": "User 4"}
    user_id = 2

    # Then
    response = await client.patch(f"/users/{user_id}", json=data,
                                  headers=headers)

    # When
    assert response.status_code == status.HTTP_403_FORBIDDEN
