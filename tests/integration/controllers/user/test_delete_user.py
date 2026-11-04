import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_users(db):
    from src.schemas.user import UserIn
    from src.services.user import UserService

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


async def test_delete_user_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    user_id = 2

    # When
    response = await client.delete(f"/users/{user_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_user_not_authenticated(client: AsyncClient):
    # Given
    user_id = 2

    # When
    response = await client.delete(f"/users/{user_id}", headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_user_not_found(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    user_id = 99

    # When
    response = await client.delete(f"/users/{user_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_user_profile_client(client: AsyncClient,
                                          access_client: str):
    # Given
    headers = {"Authorization": f"Bearer {access_client}"}
    user_id = 2

    # When
    response = await client.delete(f"/users/{user_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
