from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.employee_service import EmployeeService
from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
router = APIRouter()


@router.post("/employees", response_model=EmployeeResponse, status_code=201)
async def create_employee(employee: EmployeeCreate, session:AsyncSession = Depends(get_db)):
        service = EmployeeService(session)

        try:
             new_employee = await service.create_employee(employee)
        except ValueError:
             raise HTTPException (status_code=409, detail="Email already exists")

        return new_employee

@router.get("/employees/", response_model=list[EmployeeResponse])
async def get_all_employees(session : AsyncSession = Depends(get_db)):
    service = EmployeeService(session)
    return await service.get_all_employees()

    
            
@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, session:AsyncSession = Depends(get_db)):
        service = EmployeeService(session)
        employee = await service.get_employee(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, employee: EmployeeUpdate, session:AsyncSession = Depends(get_db)):
        service = EmployeeService(session)

        try:
            updated_employee = await service.update_employee(employee_id,employee)
            return updated_employee
        except ValueError:
             raise HTTPException (status_code= 404, detail="Employee not found")
        
@router.patch("/employees/{employee_id}", response_model=EmployeeResponse,)
async def partial_update_employee(employee_id: int, employee: EmployeeUpdate, session: AsyncSession = Depends(get_db)):
    service = EmployeeService(session)

    try:
         update_employee = await service.update_employee(employee_id,employee)
         return update_employee
    except ValueError:
         raise HTTPException (status_code= 404 , detail= "Employee not found")

@router.delete("/employees/{employee_id}", status_code=204)
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_db)):
    service = EmployeeService(session)

    try:
         await service.delete_employee(employee_id)

         return {"detail" : "Employee deleted sucessfully"}
    except ValueError:
         raise HTTPException(status_code=404, detail="Employee not found")

