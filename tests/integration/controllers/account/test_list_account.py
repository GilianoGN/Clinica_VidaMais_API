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


async def test_list_account_success(client: AsyncClient, access_admin: str):
    # Given
    params = {"limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/accounts/", params=params, headers=headers)
    content = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 2


async def test_list_account_not_authenticated(client: AsyncClient):
    # Given
    params = {"limit": 10, "skip": 0}

    # When
    response = await client.get("/accounts/", params=params)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_list_account_empty_parameters(client: AsyncClient,
                                             access_admin: str):
    # Given
    headers = {"Authorization": f"Bearer {access_admin}"}

    # When
    response = await client.get("/accounts/", params={}, headers=headers)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
