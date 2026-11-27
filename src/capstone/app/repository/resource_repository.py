from sqlalchemy.ext.asyncio import AsyncSession
from ..models.resource import Resource
from sqlalchemy import select

class ResourceRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create (self, resource_data):
        resource = Resource(**resource_data.model_dump(exclude_unset=True))
        self.session.add(resource)
        await self.session.flush()
        return resource

    async def get_all(self):
        result = await self.session.execute(select(Resource))
        return result.scalars().all()

    async def get_by_id(self, resource_id:int):
        return await self.session.get(Resource,resource_id)

    async def update(self,resource,resource_data):
        for key,value in resource_data.items():
            setattr(resource,key,value)

        await self.session.flush()
        return resource

    async def delete(self,resource):
        await self.session.delete(resource)
        await self.session.flush()



    
        


