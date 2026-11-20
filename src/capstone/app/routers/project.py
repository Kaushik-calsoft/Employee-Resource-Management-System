from fastapi import APIRouter, HTTPException, status
from ..schema.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()

projects = {}

next_id = 1

@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    global next_id
    project_id = next_id
    projects[project_id]= {
        "id": project_id,
        "name": project.name,
        "description": project.description,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "status": project.status
    }
    next_id += 1
    return projects[project_id]

@router.get("/projects/", response_model=list[ProjectResponse])
async def get_all_projects():
    return list(projects.values())

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    if project_id in projects:
        return projects[project_id]
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate):
    if project_id in projects:
        projects[project_id]["name"] = project.name
        projects[project_id]["description"] = project.description
        projects[project_id]["start_date"] = project.start_date
        projects[project_id]["end_date"] = project.end_date
        projects[project_id]["status"] = project.status
        return projects[project_id]
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def partial_update_project(project_id: int, project: ProjectUpdate):
    if project_id in projects:
        update_data = project.model_dump(exclude_unset=True)
        projects[project_id].update(update_data)
        return projects[project_id]
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/projects/{project_id}", response_model=ProjectResponse)
async def delete_project(project_id: int):
    if project_id in projects:
        deleted_project = projects.pop(project_id)
        return deleted_project
    else:
        raise HTTPException(status_code=404, detail="Project not found")

