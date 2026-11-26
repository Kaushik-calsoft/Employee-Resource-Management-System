import asyncio

from capstone.app.database import SessionLocal
from capstone.app.models.employee import Employee


async def insert_employee():
    async with SessionLocal() as session:
        employee = Employee(
            name="Test Employee",
            email="test.employee@example.com",
            designation="Python Developer",
            department="Engineering"
        )

        session.add(employee)
        await session.commit()
        await session.refresh(employee)

        print("Employee inserted successfully!")
        print("Employee ID:", employee.id)
        print("Employee Name:", employee.name)
        print("Employee Email:", employee.email)


asyncio.run(insert_employee())