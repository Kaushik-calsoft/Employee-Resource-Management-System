from pydantic import BaseModel, Field

class ResourceCreate(BaseModel):
    name: str 
    resource_type: str
    availability: bool = Field(default=True)


class ResourceUpdate(BaseModel):
    name: str = Field(None)
    resource_type: str = Field(None)
    availability: bool = Field(None)

class ResourceResponse(BaseModel):
    id: int
    name: str
    resource_type: str
    availability: bool

