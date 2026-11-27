from sqlalchemy.ext.asyncio import AsyncSession
from ..models.project import Projects
from sqlalchemy import select

class ProjectRepository:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def create(self,project_data):
        project = Projects(**project_data.model_dump(exclude_unset= True))
        self.session.add(project)
        await self.session.flush()
        return project

    async def get_all(self):
        result = await self.session.execute(select(Projects))
        return result.scalars().all()

    async def get_by_id(self,project_id:int):
        return await self.session.get(Projects, project_id)

    async def update(self, project, project_data):
        for key,value in project_data.items():
            setattr(project,key,value)

        await self.session.flush()
        return project

    async def delete(self,project):
        await self.session.delete(project)
        await self.session.flush()




