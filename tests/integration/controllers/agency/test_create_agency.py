from fastapi import status
from httpx import AsyncClient


async def test_create_agency_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"name": "Agency 1",
            "address": "Boulevard Street 13"}

    # When
    response = await client.post("/agencies/", headers=headers, json=data)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_agency_fail_duplicated_document(client: AsyncClient,
                                                      access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data1 = {"name": "Agency 1",
             "address": "Boulevard Street 13"}
    data2 = {"name": "Agency 1",
             "address": "Boulevard Street 13"}

    # When
    response1 = await client.post("/agencies/", headers=headers, json=data1)
    response2 = await client.post("/agencies/", headers=headers, json=data2)

    # Then
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_409_CONFLICT


async def test_create_agency_invalid_data(client: AsyncClient,
                                          access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"name": "Agency 1"}

    # When
    response = await client.post("/agencies/", headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_create_agency_not_authenticated(client: AsyncClient):
    # Given
    data = {"name": "Agency 1",
            "address": "Boulevard Street 13"}

    # When
    response = await client.post("/agencies/", headers={}, json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_agency_profile_client(client: AsyncClient,
                                            access_client: str):
    # Given
    headers = {"Authorization": f"Bearer {access_client}"}
    data = {"name": "Agency 1",
            "address": "Boulevard Street 13"}

    # When
    response = await client.post("/agencies/", headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
