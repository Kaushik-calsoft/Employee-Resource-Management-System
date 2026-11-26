from sqlalchemy import select
from ..database import SessionLocal
from ..models.employee import Employee
from fastapi import APIRouter, HTTPException, status
from ..schema.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
router = APIRouter()


@router.post("/employees", response_model=EmployeeResponse, status_code=201)
async def create_employee(employee: EmployeeCreate):
    async with SessionLocal() as session:
        result = await session.execute(select(Employee).where(Employee.email == employee.email))
        existing_employee = result.scalars().first()
        if existing_employee:
            raise HTTPException(
                status_code = 409,
                detail="Email already exists"
            )
        
        new_employee = Employee(
            name=employee.name,
            email=employee.email,
            designation=employee.designation,
            department=employee.department,
        )

        session.add(new_employee)
        await session.commit()
        await session.refresh(new_employee)
        return new_employee

@router.get("/employees/", response_model=list[EmployeeResponse])
async def get_all_employees():
    async with SessionLocal() as session:
        result = await session.execute(select(Employee))
        employees = result.scalars().all()
        return employees

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int):
    async with SessionLocal() as session:
        employee = await session.get(Employee,employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, employee: EmployeeUpdate):
    async with SessionLocal() as session:
        existing_employee = await session.get(Employee,employee_id)
        if existing_employee is None:
            raise HTTPException(
                status_code = 404,
                detail = "Employee not found"
            )

        existing_employee.name = employee.name
        existing_employee.email = employee.email
        existing_employee.designation = employee.designation
        existing_employee.department = employee.department

        await session.commit()
        await session.refresh(existing_employee)

        return existing_employee
        
@router.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def partial_update_employee(employee_id: int, employee: EmployeeUpdate):
    async with SessionLocal() as session:
        existing_employee = await session.get(Employee, employee_id)
        if existing_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        update_data = employee.model_dump(exclude_unset=True)

        for field,values in update_data.items():
            setattr(existing_employee,field,values)

        await session.commit()
        await session.refresh(existing_employee)

        return existing_employee
        
@router.delete("/employees/{employee_id}", response_model=EmployeeResponse)
async def delete_employee(employee_id: int):
    async with SessionLocal() as session:
        existing_employee = await session.get(Employee,employee_id)

        if existing_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        await session.delete(existing_employee)
        await session.commit()

        return existing_employee
