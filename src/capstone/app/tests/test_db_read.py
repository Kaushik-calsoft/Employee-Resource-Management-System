import asyncio

from sqlalchemy import select
from capstone.app.database import SessionLocal
from capstone.app.models.employee import Employee


async def read_employee():
    async with SessionLocal() as session:
        result = await session.execute(select(Employee))
        employees = result.scalars().all()

        for employee in employees:
            print(
                employee.id,
                employee.name,
                employee.email,
                employee.designation,
                employee.department
            )

    await SessionLocal.kw["bind"].dispose()


asyncio.run(read_employee())