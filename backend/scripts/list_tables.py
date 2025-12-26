import asyncio
from app.db.session import engine
from sqlalchemy import text

async def list_tables():
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        )
        tables = [row[0] for row in result]
        print("Database tables:")
        for table in tables:
            print(f"  - {table}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(list_tables())
