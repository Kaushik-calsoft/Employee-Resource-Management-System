from pydantic import BaseModel, Field
from datetime import date

class AssignmentCreate(BaseModel):
    employee_id: int
    project_id: int
    resource_id: int
    assigned_dates: date
    status: str = "active"

class AssignmentUpdate(BaseModel):
    employee_id: int | None = None
    project_id: int | None = None
    resource_id: int | None = None
    assigned_dates: date | None = None
    status: str | None = None

class AssignmentResponse(BaseModel):
    id: int
    employee_id: int
    project_id: int
    resource_id: int
    assigned_dates: date
    status: str

