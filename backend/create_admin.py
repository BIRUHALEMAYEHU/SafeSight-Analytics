import asyncio
import os
import sys

# Add the current directory to sys.path to find 'app'
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.models.user import User
from app.core.config import settings

async def create_first_user():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Check if admin already exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.username == "admin"))
        if result.scalars().first():
            print("Admin user already exists.")
            return

        user = User(
            username="admin",
            email="admin@safesight.io",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(user)
        try:
            await db.commit()
            print("Admin user created successfully! (User: admin, Pass: admin123)")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_first_user())
