from sqlalchemy import select
from ..models.assignment import Assignment
from ..database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from ..schema.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse

router = APIRouter()


@router.post("/assignments", response_model=AssignmentResponse, status_code=201)
async def create_assignment(assignment: AssignmentCreate):
    async with SessionLocal() as session:
        result = await session.execute(select(Assignment).where(
            Assignment.employee_id == assignment.employee_id,
            Assignment.project_id == assignment.project_id,
            Assignment.resource_id == assignment.resource_id
        ))
        existing_record = result.scalars().first()


        if existing_record is not None:
            raise HTTPException (status_code = 409, detail = "Record already exists")

        new_assign = Assignment(
            employee_id = assignment.employee_id,
            project_id = assignment.project_id,
            resource_id = assignment.resource_id,
            assigned_dates = assignment.assigned_dates,
            status = assignment.status
        )

        session.add(new_assign)
        await session.commit()
        await session.refresh(new_assign)

        return new_assign
    
@router.get("/assignments", response_model=list[AssignmentResponse])
async def get_assignments():
    async with SessionLocal() as session:
        result = await session.execute(select(Assignment))
        assignment = result.scalars().all()
    return assignment

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int):
    async with SessionLocal() as session:
        assign_id = await session.get(Assignment, assignment_id)
        if assign_id is None:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
    return assign_id

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate):
    async with SessionLocal() as session:
        assign = await session.get(Assignment, assignment_id)
        if assign is None:
            raise HTTPException(status_code=404, detail="Assignment not found")

        assign.employee_id = assignment_update.employee_id
        assign.project_id = assignment_update.project_id
        assign.resource_id = assignment_update.resource_id
        assign.assigned_dates = assignment_update.assigned_dates
        assign.status = assignment_update.status

        await session.commit()
        await session.refresh(assign)

        return  assign
@router.patch("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def partial_update_assignment(assignment_id: int, assignment_update: AssignmentUpdate):
    async with SessionLocal() as session:
        assign_id = await session.get(Assignment , assignment_id)
        if assign_id is None:
            raise HTTPException(status_code= 404, detail="Assignment not found")
        assign = assignment_update.model_dump(exclude_unset=True)

        for field,value in assign.items():
            setattr(assign_id,field,value)

        await session.commit()
        await session.refresh(assign_id)

        return assign_id

@router.delete("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def delete_assignment(assignment_id: int):
    async with SessionLocal() as session:
        result = await session.get(Assignment, assignment_id)
        if result is None:
            raise HTTPException (status_code= 404, detail= "Assingnment not found")

        await session.delete(result)
        await session.commit()

        return result
