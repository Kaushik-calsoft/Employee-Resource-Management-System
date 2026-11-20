from fastapi import APIRouter, HTTPException, status
from ..schema.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
router = APIRouter()

users = {}

next_id = 101


@router.post("/employees", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate):
    global next_id
    user_id = next_id
    users[user_id] = {
        "id": user_id,
        "name": employee.name,
        "email": employee.email,
        "designation": employee.designation,
        "department": employee.department
    }
    next_id += 1
    return {"id": user_id, **users[user_id]}

@router.get("/employees/", response_model=list[EmployeeResponse])
async def get_all_employees():
    return list(users.values())

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int):
    if employee_id in users:
        return users[employee_id]
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, employee: EmployeeUpdate):
    if employee_id in users:
        users[employee_id]["name"] = employee.name
        users[employee_id]["email"] = employee.email
        users[employee_id]["designation"] = employee.designation
        users[employee_id]["department"] = employee.department
        return users[employee_id]
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def partial_update_employee(employee_id: int, employee: EmployeeUpdate):
    if employee_id in users:
        update_data = employee.model_dump(exclude_unset=True)
        users[employee_id].update(update_data)
        return users[employee_id]
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/employees/{employee_id}", response_model=EmployeeResponse)
async def delete_employee(employee_id: int):
    if employee_id in users:
        deleted_employee = users.pop(employee_id)
        return deleted_employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


    