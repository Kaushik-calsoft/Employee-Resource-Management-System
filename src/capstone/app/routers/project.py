from sqlalchemy.ext.asyncio import AsyncSession
from ..services.projects_service import ProjectService
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse , status_code= 201)
async def create_project(project: ProjectCreate, session: AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    new_project = await service.create_project(project)
    return new_project
    
@router.get("/projects/", response_model=list[ProjectResponse])
async def get_all_projects(session:AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    return await service.get_all_project()


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, session: AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    existing = await service.get_by_id(project_id)

    if existing is None:
        raise HTTPException (status_code=404, detail="project not found")

    return existing
    
@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate, session:AsyncSession = Depends(get_db)):
    service = ProjectService(session)

    try: 
        updated_project = await service.update_project(project_id,project)
        return updated_project
    except ValueError:
        raise HTTPException (status_code=404, detail="project not found")
    

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def partial_update_project(project_id: int, project: ProjectUpdate, session:AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    try:
        updated_project = await service.update_project(project_id,project)
        return updated_project
    except ValueError as e:
        if str(e) =="Project Not found":
            raise HTTPException(status_code=404, detail="project not found")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, session:AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    try:
        await service.delete_project(project_id)
        return {"detail":"Project deleted sucessfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="project not found")
