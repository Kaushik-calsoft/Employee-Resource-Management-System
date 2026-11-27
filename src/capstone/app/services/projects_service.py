from sqlalchemy.ext.asyncio import AsyncSession
from ..repository.projects_repository import ProjectRepository

class ProjectService:
    def __init__(self,session:AsyncSession):
        self.session = session
        self.repository = ProjectRepository(session)

    async def create_project(self,project):

        try:
            new_project = await self.repository.create(project)
            await self.session.commit()
            return new_project
        except:
            await self.session.rollback()
            raise

    async def get_all_project(self):
        return await self.repository.get_all()

    async def get_by_id(self,project_id:int):
        return await self.repository.get_by_id(project_id)

    async def update_project(self,project_id:int, project_data):
        existing = await self.repository.get_by_id(project_id)

        if existing is None:
            raise ValueError("Project not found")

        
        updated_data = project_data.model_dump(exclude_unset = True)

        start_date = updated_data.get("start_date", existing.start_date)
        end_date = updated_data.get("end_date", existing.end_date)

        if start_date and end_date and end_date < start_date:
            raise ValueError ("End date must be after start date")

        try:
            updated_project = await self.repository.update(existing,updated_data)
            await self.session.commit()
            return updated_project
        except :
            await self.session.rollback()
            raise

    async def delete_project(self, project_id:int):
        existing = await self.repository.get_by_id(project_id)
        if existing is None:
            raise ValueError("Project not found")

        try:
            await self.repository.delete(existing)
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

        
    


    
    
        