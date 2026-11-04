from fastapi import status
from httpx import AsyncClient


async def test_create_user_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"name": "user 1",
            "document": "12345678900",
            "profile": "client",
            "password": "123456"}

    # When
    response = await client.post("/users/", headers=headers, json=data)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_user_fail_duplicated_document(client: AsyncClient,
                                                    access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data1 = {"name": "user 1",
             "document": "11111111111",
             "profile": "client",
             "password": "123456"}
    data2 = {"name": "user 2",
             "document": "11111111111",
             "profile": "client",
             "password": "123456"}

    # When
    response1 = await client.post("/users/", headers=headers, json=data1)
    response2 = await client.post("/users/", headers=headers, json=data2)

    # Then
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_409_CONFLICT


async def test_create_user_invalid_data(client: AsyncClient,
                                        access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"document": "12345678900",
            "profile": "client",
            "password": "123456"}

    # When
    response = await client.post("/users/", headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_create_user_not_authenticated(client: AsyncClient):
    # Given
    data = {"name": "user 1",
            "document": "12345678900",
            "profile": "client",
            "password": "123456"}

    # When
    response = await client.post("/users/", headers={}, json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_user_profile_client(client: AsyncClient,
                                          access_client: str):
    # Given
    headers = {"Authorization": f"Bearer {access_client}"}
    data = {"name": "user 1",
            "document": "12345678900",
            "profile": "client",
            "password": "123456"}

    # When
    response = await client.post("/users/", headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
