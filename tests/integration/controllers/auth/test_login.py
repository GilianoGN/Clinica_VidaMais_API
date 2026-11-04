from fastapi import status
from httpx import AsyncClient


async def test_login_success(client: AsyncClient):
    # Given
    data = {"username": "Test User Admin",
            "password": "123456"}

    # When
    response = await client.post("/auth/login", json=data)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None


async def test_login_invalid_credentials(client: AsyncClient):
    # Given
    data = {"username": "Test User Admin",
            "password": "abcdef"}

    # When
    response = await client.post("/auth/login", json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
