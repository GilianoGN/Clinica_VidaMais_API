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

    accservice = AccountService()
    await accservice.create(user_id=1,
                            account=AccountIn(agency_id=1, type="corrente"))
    await accservice.create(user_id=2,
                            account=AccountIn(agency_id=1, type="poupanca"))

    from src.schemas.transaction import TransactionIn
    from src.services.transaction import TransactionService

    service = TransactionService()
    await service.create_deposit(
        TransactionIn(account_id=1, type="deposito", statement_type="credit",
                      amount=10000.00))
    await service.create_withdrawal(
        TransactionIn(account_id=1, type="saque", statement_type="debit",
                      amount=500.00))
    await service.create_transfer(
        TransactionIn(account_id=1,
                      destination_account_id=2,
                      type="transferencia",
                      statement_type="credit",
                      amount=1000.00))


async def test_statement_all_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    params = {"account_id": 1, "statement": "all", "limit": 10, "skip": 0}

    # When
    response = await client.get(
        f"/transactions/statement/{params['account_id']}",
        params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 3


async def test_statement_credit_success(client: AsyncClient,
                                        access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    params = {"account_id": 1, "statement": "credit", "limit": 10, "skip": 0}

    # When
    response = await client.get(
        f"/transactions/statement/{params['account_id']}",
        params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1


async def test_statement_debit_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    params = {"account_id": 1, "statement": "debit", "limit": 10, "skip": 0}

    # When
    response = await client.get(
        f"/transactions/statement/{params['account_id']}",
        params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 2


async def test_statement_not_authenticated(client: AsyncClient):
    # Given
    params = {"account_id": 1, "statement": "all", "limit": 10, "skip": 0}

    # When
    response = await client.get(
        f"/transactions/statement/{params['account_id']}",
        params=params, headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_statement_not_found(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    params = {"account_id": 99, "statement": "all", "limit": 10, "skip": 0}

    # When
    response = await client.get(
        f"/transactions/statement/{params['account_id']}",
        params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_statement_empty_parameters(client: AsyncClient,
                                          access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    account_id = 1

    # When
    response = await client.get(
        f"/transactions/statement/{account_id}", params={}, headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
