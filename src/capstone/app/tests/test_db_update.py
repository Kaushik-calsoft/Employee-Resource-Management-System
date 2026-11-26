import asyncio

from capstone.app.database import SessionLocal, engine
from capstone.app.models.employee import Employee


async def update_employee():
    try:
        async with SessionLocal() as session:
            employee = await session.get(Employee, 1)

            if employee is None:
                print("Employee not found!")
                return

            employee.designation = "Senior Python Developer"
            employee.department = "Platform Engineering"

            await session.commit()
            await session.refresh(employee)

            print("Employee updated successfully!")
            print("ID:", employee.id)
            print("Name:", employee.name)
            print("Designation:", employee.designation)
            print("Department:", employee.department)

    finally:
        await engine.dispose()


asyncio.run(update_employee())