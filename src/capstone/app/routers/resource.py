from sqlalchemy.ext.asyncio import AsyncSession
from ..services.resource_service import ResourceService
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from ..schema.resource import ResourceCreate, ResourceUpdate, ResourceResponse


router = APIRouter()

@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(resource: ResourceCreate, session:AsyncSession = Depends(get_db)):
    service = ResourceService(session)
    new_resource = await  service.create_resource(resource)
    
    return new_resource
   
@router.get("/resources", response_model=list[ResourceResponse])
async def get_resources(session:AsyncSession = Depends(get_db)):
    service = ResourceService(session)
    return await service.get_all_resource()

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, session:AsyncSession = Depends(get_db)):
    service = ResourceService(session)
    existing = await service.get_by_id(resource_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="resource not found")

    return existing

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource_update: ResourceUpdate, session:AsyncSession = Depends(get_db)):
    service = ResourceService(session)

    try : 
        updated_resource = await service.update_resource(resource_id,resource_update)
        return updated_resource
    except ValueError:
        raise HTTPException (status_code=404, detail="Resource not found")
        
@router.patch("/resources/{resource_id}", response_model=ResourceResponse)
async def partial_update_resource(resource_id: int, resource_update: ResourceUpdate, session:AsyncSession = Depends(get_db)):
    
    service = ResourceService(session)

    try:
        updated_resource = await service.update_resource(resource_id, resource_update)
        return updated_resource
    except ValueError:
        raise HTTPException (status_code=404, detail="Resource not found")
    

@router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: int, session:AsyncSession = Depends(get_db)):
    service = ResourceService(session)

    try:
        await service.delete_resource(resource_id)
        return {"detail" : "Deleted resource sucessfully"}

    except ValueError:
        raise HTTPException(status_code=404, detail="Resource not found")
