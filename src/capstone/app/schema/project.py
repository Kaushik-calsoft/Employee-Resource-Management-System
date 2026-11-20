from pydantic import BaseModel , Field , model_validator
from datetime import date

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    start_date: date
    end_date: date
    status: str
    @model_validator(mode='after')
    @classmethod
    def validate_dates(cls, self):
        if self.start_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date")
        return self.end_date

class ProjectUpdate(BaseModel):
    name : str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    @model_validator(mode='after')
    @classmethod
    def validate_dates(cls, self):
            if self.start_date and self.end_date < self.start_date:
                raise ValueError("End date cannot be earlier than start date")
            return self.end_date
    

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    start_date: date
    end_date: date
    status: str


