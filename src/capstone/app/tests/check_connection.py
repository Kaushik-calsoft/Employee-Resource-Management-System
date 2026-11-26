
import asyncio
from sqlalchemy import text
from capstone.app.database import engine

async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Connection successful:", result.scalar())

    except Exception as e:
        print("Connection failed:", e)

    finally:
        await engine.dispose()

asyncio.run(test_connection())
