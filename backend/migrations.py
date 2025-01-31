import asyncio
from app.database import engine
from app.models import Base
from app.services import UserService
from app.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def create_initial_data():
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        
        # Create test user
        test_user = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User"
        )
        await user_service.create_user(test_user)

async def main():
    print("Creating tables...")
    await create_tables()
    print("Creating initial data...")
    await create_initial_data()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())