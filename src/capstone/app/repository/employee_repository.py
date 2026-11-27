from sqlalchemy.ext.asyncio import AsyncSession
from ..models.employee import Employee
from sqlalchemy import select

class EmployeeRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_by_id(self,employee_id:int):
        return await self.session.get(Employee, employee_id)

    async def get_all(self):
        result = await self.session.execute(select(Employee))
        return result.scalars().all()
    
    async def create(self,employee_data):
        employee = Employee(**employee_data.model_dump())
        self.session.add(employee)
        await self.session.flush()
        return employee
    
    async def get_by_email(self, email: str):
        result = await self.session.execute(
        select(Employee).where(Employee.email == email)
        )
        return result.scalars().first()

    async def update(self,employee,employee_data):
        for key,value in employee_data.items():
            setattr(employee,key,value)

        await self.session.flush()
        return employee

    async def delete(self,employee):
        await self.session.delete(employee)
        await self.session.flush()

