from sqlalchemy.ext.asyncio import AsyncSession
from ..repository.resource_repository import ResourceRepository


class ResourceService:
    def __init__(self, session):
        self.session = session
        self.repository = ResourceRepository(session)

    async def create_resource(self,resource):
        try:
            new_resource = await self.repository.create(resource)
            await self.session.commit()
            return new_resource
        except :
            await self.session.rollback()
            raise

    async def get_all_resource(self):
        return await self.repository.get_all()

    async def get_by_id(self,resource_id:int):
        return await self.repository.get_by_id(resource_id)

    async def update_resource(self,resource_id:int, resource_data):
        existing = await self.repository.get_by_id(resource_id)

        if existing is None:
            raise ValueError("Resource not found")

        try:
            updated_resource = await self.repository.update(existing, resource_data.model_dump(exclude_unset = True))
            await self.session.commit()
            return updated_resource
        except:
            await self.session.rollback()
            raise

    async def delete_resource(self,resource_id:int):
        existing = await self.repository.get_by_id(resource_id)

        if existing is None:
            raise ValueError("Resource not found")

        try:
            await self.repository.delete(existing)
            await self.session.commit()

        except:
            await self.session.rollback()
            raise
