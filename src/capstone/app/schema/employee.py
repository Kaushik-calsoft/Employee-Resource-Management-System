from pydantic import BaseModel, Field , EmailStr

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., unique=True)
    designation: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)

class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100) 
    email: EmailStr | None = Field(default=None)
    designation: str | None = Field(default=None, min_length=1, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    designation: str
    department: str