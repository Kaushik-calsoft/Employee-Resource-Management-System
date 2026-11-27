from sqlalchemy.ext.asyncio import AsyncSession
from ..models.assignment import Assignment
from sqlalchemy import select

class AssignmentRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self, assignment_data):
        assignment = Assignment(assignment_data.model_dump(exclude_unset = True))
        self.session.add(assignment)
        self.session.commit()
        await self.session.flush()
        return assignment

    async def get_all(self):
        result = await self.session.execute(select(Assignment))
        return await result.scalars().all()

    async def get_by_id(self, assignment_id:int):
        return await self.session.get(assignment_id)

    async def update(self, assignment_id, assignment):
        for key,value in assignment.items():
            setattr(assignment_id,key,value)

        await self.session.flush()
        return assignment

    async def delete(self, assignment):
            await self.session.delete(assignment)
            await self.sessiom.flush()



    

        
