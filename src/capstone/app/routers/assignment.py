from fastapi import APIRouter, HTTPException, status
from ..schema.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse

router = APIRouter()

assignments = {}

next_id = 1

@router.post("/assignments", response_model=AssignmentResponse)
async def create_assignment(assignment: AssignmentCreate):
    global next_id
    assignment_id = next_id
    assignments[assignment_id] = {
        "id": assignment_id,
        "employee_id": assignment.employee_id,
        "project_id": assignment.project_id,
        "resource_id": assignment.resource_id,
        "assigned_date": assignment.assigned_date,
        "status": assignment.status
    }
    next_id += 1
    return assignments[assignment_id]

@router.get("/assignments", response_model=list[AssignmentResponse])
async def get_assignments():
    return list(assignments.values())

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int):
    if assignment_id not in assignments:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignments[assignment_id]

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate):
    if assignment_id in assignments:
        assignments[assignment_id]["employee_id"] = assignment_update.employee_id
        assignments[assignment_id]["project_id"] = assignment_update.project_id
        assignments[assignment_id]["resource_id"] = assignment_update.resource_id
        assignments[assignment_id]["assigned_date"] = assignment_update.assigned_date
        return assignments[assignment_id]
    else:
        raise HTTPException(status_code=404, detail="Assignment not found")

@router.patch("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def partial_update_assignment(assignment_id: int, assignment_update: AssignmentUpdate):
    if assignment_id in assignments:
        update_data = assignment_update.model_dump(exclude_unset=True)
        assignments[assignment_id].update(update_data)
        return assignments[assignment_id]
    else:
        raise HTTPException(status_code=404, detail="Assignment not found")

@router.delete("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def delete_assignment(assignment_id: int):
    if assignment_id in assignments:
        deleted_assignment = assignments.pop(assignment_id)
        return deleted_assignment
    else:
        raise HTTPException(status_code=404, detail="Assignment not found")

