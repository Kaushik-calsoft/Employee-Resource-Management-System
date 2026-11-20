from fastapi import APIRouter, Depends, HTTPException
from ..schema.resource import ResourceCreate, ResourceUpdate, ResourceResponse


router = APIRouter()

resource = {}

next_id = 1

@router.post("/resources", response_model=ResourceResponse)
async def create_resource(resource: ResourceCreate):
    global next_id
    resource_id = next_id
    resource[resource_id] = {
        "id": resource_id,
        "name": resource.name,
        "description": "",
        "resource_type": resource.resource_type,
        "availability": resource.availability
    }
    next_id += 1
    return resource[resource_id]

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    if resource_id not in resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource[resource_id]

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource_update: ResourceUpdate):
    if resource_id in resource:
        resource[resource_id]["name"] = resource_update.name
        resource[resource_id]["resource_type"] = resource_update.resource_type
        resource[resource_id]["availability"] = resource_update.availability
        return resource[resource_id]
    else:
        raise HTTPException(status_code=404, detail="Resource not found")

@router.patch("/resources/{resource_id}", response_model=ResourceResponse)
async def partial_update_resource(resource_id: int, resource_update: ResourceUpdate):
    if resource_id in resource:
        update_data = resource_update.model_dump(exclude_unset=True)
        resource[resource_id].update(update_data)
        return resource[resource_id]
    else:
        raise HTTPException(status_code=404, detail="Resource not found")

@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
async def delete_resource(resource_id: int):
    if resource_id in resource:
        deleted_resource = resource.pop(resource_id)
        return deleted_resource
    else:
        raise HTTPException(status_code=404, detail="Resource not found")

