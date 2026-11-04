import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_account(db):
    from src.schemas.agency import AgencyIn
    from src.services.agency import AgencyService

    agencyservice = AgencyService()
    await agencyservice.create(AgencyIn(name="Agency 1",
                                        address="Boulevard Street 13"))

    from src.schemas.account import AccountIn
    from src.services.account import AccountService

    service = AccountService()
    await service.create(user_id=1,
                         account=AccountIn(agency_id=1, type="corrente"))
    await service.update(user_id=1, account_id=1, balance=100.0)


async def test_create_deposit_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "type": "deposito",
            "statement_type": "credit",
            "amount": 1000.00}

    # When
    response = await client.post("/transactions/deposit",
                                 headers=headers, json=data)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_deposit_invalid_data(client: AsyncClient,
                                           access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "type": "deposito",
            "amount": 1000.00}

    # When
    response = await client.post("/transactions/deposit",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_create_deposit_not_authenticated(client: AsyncClient):
    # Given
    data = {"account_id": 1,
            "type": "deposito",
            "statement_type": "credit",
            "amount": 1000.00}

    # When
    response = await client.post("/transactions/deposit",
                                 headers={}, json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_deposit_not_found(client: AsyncClient,
                                        access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 99,
            "type": "deposito",
            "statement_type": "credit",
            "amount": 1000.00}

    # When
    response = await client.post("/transactions/deposit",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_deposit_type_invalid(client: AsyncClient,
                                           access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "type": "saque",
            "statement_type": "credit",
            "amount": 1000.00}

    # When
    response = await client.post("/transactions/deposit",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
