from sqlalchemy.ext.asyncio import AsyncSession
from..repository.assignments_repository import AssignmentRepository
from sqlalchemy import select

class AssignmentService:
    def __init__(self, session:AsyncSession):
        self.session = session
        self.repository = AssignmentRepository(session)

    async def create_assign(self,assignment):
        try:
            new_assignment = await self.repository.create(assignment)
            await self.session.commit()
            return new_assignment
        except :
            self.session.rollback()
            raise

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, assignment_id:int):
        return await self.repository.get_by_id(assignment_id)

    async def update(self, assignment_id , assignment):
        existing = await self.repository.get_by_id(assignment_id)

        if existing is None:
            raise ValueError("Assignment is not found")

        try:
            updated_assignment = await self.repository.update(existing,assignment.model_dump(exclude_unset=True))
            await self.session.commit()
            return updated_assignment
        except:
            self.session.rollback()
            raise

    async def delete(self, assign_id):
        existing  = await self.repository.get_by_id(assign_id)

        if existing is None:
             raise ValueError("Assignment not found")

        try:
            await self.repository.delete(existing)
            await self.session.commit()

        except:
            await self.session.rollback
            raise




