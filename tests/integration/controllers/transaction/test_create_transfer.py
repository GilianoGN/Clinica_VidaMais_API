import pytest_asyncio
from fastapi import status  # noqa
from httpx import AsyncClient  # noqa


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
    await service.create(user_id=2,
                         account=AccountIn(agency_id=1, type="poupanca"))
    await service.update(user_id=1, account_id=1, balance=1000.0)


async def test_create_deposit_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "destination_account_id": 2,
            "type": "transferencia",
            "statement_type": "debit",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
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
            "destination_account_id": 2,
            "type": "transferencia",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_create_deposit_not_authenticated(client: AsyncClient):
    # Given
    data = {"account_id": 1,
            "destination_account_id": 2,
            "type": "transferencia",
            "statement_type": "debit",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers={}, json=data)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_deposit_not_found(client: AsyncClient,
                                        access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "destination_account_id": 99,
            "type": "transferencia",
            "statement_type": "debit",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_deposit_type_invalid(client: AsyncClient,
                                           access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "destination_account_id": 2,
            "type": "saque",
            "statement_type": "debit",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_create_deposit_insufficient_balance(client: AsyncClient,
                                                   access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "destination_account_id": 2,
            "type": "transferencia",
            "statement_type": "debit",
            "amount": 2500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_create_deposit_account_not_diferent(client: AsyncClient,
                                                   access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    data = {"account_id": 1,
            "destination_account_id": 1,
            "type": "transferencia",
            "statement_type": "debit",
            "amount": 500.00}

    # When
    response = await client.post("/transactions/transfer",
                                 headers=headers, json=data)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
