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
    await service.create(user_id=1,
                         account=AccountIn(agency_id=1, type="poupanca"))
    await service.create(user_id=2,
                         account=AccountIn(agency_id=1, type="poupanca"))
    await service.update(user_id=1, account_id=1, balance=100.0)


async def test_delete_account_success(client: AsyncClient, access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    account_id = 2

    # When
    response = await client.delete(f"/accounts/{account_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_account_not_authenticated(client: AsyncClient):
    # Given
    account_id = 2

    # When
    response = await client.delete(f"/accounts/{account_id}", headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_account_not_found(client: AsyncClient,
                                        access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    account_id = 99

    # When
    response = await client.delete(f"/accounts/{account_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_account_not_permition(client: AsyncClient,
                                            access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    account_id = 3

    # When
    response = await client.delete(f"/accounts/{account_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_delete_account_not_balance_zero(client: AsyncClient,
                                               access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}
    account_id = 1

    # When
    response = await client.delete(f"/accounts/{account_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
