import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from src.config import settings
from passlib.context import CryptContext


settings.database_url = "sqlite:///tests.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest_asyncio.fixture(autouse=True)
async def db(request):
    from src.database import database, engine, metadata  # noqa
    from models.mo_user import users  # noqa
    from src.models.agency import agencies  # noqa
    from src.models.account import accounts  # noqa
    from src.models.transaction import transactions  # noqa

    await database.connect()
    metadata.create_all(engine)

    for table in reversed(metadata.sorted_tables):
        await database.execute(table.delete())

    # Criar um usuário no banco para teste
    await database.execute(
        users.insert().values(
            name="Test User Admin",
            document="00000000000",
            profile="admin",
            password=pwd_context.hash("123456")
        )
    )
    await database.execute(
        users.insert().values(
            name="Test User Client",
            document="99999999999",
            profile="client",
            password=pwd_context.hash("123456")
        )
    )

    def teardown():
        async def _teardown():
            await database.disconnect()
            metadata.drop_all(engine)

        asyncio.run(_teardown())

    request.addfinalizer(teardown)


@pytest_asyncio.fixture
async def client(db):
    from src.main import app

    transport = ASGITransport(app=app)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with AsyncClient(base_url="http://test",
                           transport=transport,
                           headers=headers) as client:
        yield client


@pytest_asyncio.fixture
async def access_admin(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"username": "Test User Admin",
              "password": "123456"})
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def access_client(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"username": "Test User Client",
              "password": "123456"})
    return response.json()["access_token"]
