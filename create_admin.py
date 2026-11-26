import asyncio
from passlib.context import CryptContext
from src.database import database
from models.mo_user import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_initial_admin():
    await database.connect()

    try:
        query = users.select()
        existing_users = await database.fetch_all(query)
        if not existing_users:
            insert_query = users.insert().values(
                name="administrador",
                document="00000000000",
                profile="admin",
                password=pwd_context.hash("admin123")
            )
            await database.execute(insert_query)
            print("Superusuário criado com sucesso!")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(create_initial_admin())
