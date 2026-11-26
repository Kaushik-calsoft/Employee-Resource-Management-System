from sqlalchemy import select
from ..database import SessionLocal
from ..models.resource import Resource
from fastapi import APIRouter, Depends, HTTPException
from ..schema.resource import ResourceCreate, ResourceUpdate, ResourceResponse


router = APIRouter()

@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(resource: ResourceCreate):
    async with SessionLocal() as session:
        new_resource = Resource(
            name = resource.name,
            resource_type = resource.resource_type,
            availability = resource.availability
        )

        session.add(new_resource)
        await session.commit()
        await session.refresh(new_resource)

        return new_resource
   
@router.get("/resources", response_model=list[ResourceResponse])
async def get_resources():
    async with SessionLocal() as session:
        result = await session.execute(select(Resource))
        resource = result.scalars().all()
    return resource

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    async with SessionLocal() as session:
        resource = await session.get(Resource, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        return resource

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource_update: ResourceUpdate):
    async with SessionLocal() as session:
        resource = await session.get(Resource, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        resource.name = resource_update.name
        resource.resource_type = resource_update.resource_type
        resource.availability = resource_update.availability

        await session.commit()
        await session.refresh(resource)

        return resource

@router.patch("/resources/{resource_id}", response_model=ResourceResponse)
async def partial_update_resource(resource_id: int, resource_update: ResourceUpdate):
    async with SessionLocal() as session:
        resource = await session.get(Resource, resource_id)
        if resource is None:
            raise HTTPException( status_code=404, detail="Resource not found")

        update = resource_update.model_dump(exclude_unset=True)

        for field,value in update.items():
            setattr(resource,field,value)

        await session.commit()
        await session.refresh(resource)

        return resource
@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
async def delete_resource(resource_id: int):
    async with SessionLocal() as session:
        res_id = await session.get(Resource, resource_id)
        if res_id is None:
            raise HTTPException( status_code=404, detail="Resource not found")

        await session.delete(res_id)
        await session.commit()

        return res_id