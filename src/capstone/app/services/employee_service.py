from sqlalchemy.ext.asyncio import AsyncSession
from ..repository.employee_repository import EmployeeRepository

class EmployeeService:
    def __init__(self,session:AsyncSession):
        self.session = session
        self.repository = EmployeeRepository(session)

    async def get_employee(self,employee_id:int):
        return await self.repository.get_by_id(employee_id)
    
    async def get_all_employees(self):
        return await self.repository.get_all()

    async def create_employee(self,employee):
        exising = await self.repository.get_by_email(employee.email)

        if exising:
            raise ValueError ("Email already registerd")
        try :
            new_employee = await self.repository.create(employee)
            await self.session.commit()
            return new_employee
        except:
            await self.session.rollback()
            raise

    async def update_employee(self,employee_id: int , employee_data):
        existing = await self.repository.get_by_id(employee_id)

        if existing is None:
            raise ValueError("Employee not found")

        try :
            updated_employee = await self.repository.update(existing, employee_data.model_dump(exclude_unset=True))
            await self.session.commit()
            return updated_employee
        except Exception:
            await self.session.rollback()
            raise

    async def delete_employee(self,employee_id:int):
        existing  = await self.repository.get_by_id(employee_id)
        if existing is None:
            raise ValueError ("Employee Not found")
        try :
            await self.repository.delete(existing)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise

