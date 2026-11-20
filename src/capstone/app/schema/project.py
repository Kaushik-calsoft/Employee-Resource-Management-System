from pydantic import BaseModel , Field
from datetime import date

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    start_date: date
    end_date: date
    status: str

class ProjectUpdate(BaseModel):
    name : str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    start_date: date
    end_date: date
    status: str


