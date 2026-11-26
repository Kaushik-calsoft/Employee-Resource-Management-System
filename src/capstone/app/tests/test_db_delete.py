import asyncio

from capstone.app.database import SessionLocal, engine
from capstone.app.models.employee import Employee


async def delete_employee():
    try:
        async with SessionLocal() as session:
            employee = await session.get(Employee, 1)

            if employee is None:
                print("Employee not found!")
                return

            await session.delete(employee)
            await session.commit()

            print("Employee deleted successfully!")

    finally:
        await engine.dispose()


asyncio.run(delete_employee())