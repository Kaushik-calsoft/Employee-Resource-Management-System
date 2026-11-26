from sqlalchemy import select
from ..database import SessionLocal
from ..models.project import Projects
from fastapi import APIRouter, HTTPException, status
from ..schema.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse , status_code= 201)
async def create_project(project: ProjectCreate):
    async with SessionLocal() as session:
        new_project = Projects(
            name = project.name,
            description = project.description,
            start_date = project.start_date,
            end_date = project.end_date,
            status = project.status
        )
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)

    return new_project
    
@router.get("/projects/", response_model=list[ProjectResponse])
async def get_all_projects():
    async with SessionLocal() as session:
        result = await session.execute(select(Projects))
        projects = result.scalars().all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    async with SessionLocal() as session:
        project = await session.get(Projects,project_id)
        if project is None:
            raise HTTPException(status_code=404 , detail= "Project not found")

    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate):
    async with SessionLocal() as session:
        update_project = await session.get(Projects, project_id)

        if update_project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        update_project.name = project.name
        update_project.description = project.description
        update_project.start_date = project.start_date
        update_project.end_date = project.end_date
        update_project.status = project.status

        await session.commit()
        await session.refresh(update_project)

        return update_project

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def partial_update_project(project_id: int, project: ProjectUpdate):
    async with SessionLocal() as session:
        project_id = await session.get(Projects, project_id)
        if project_id is None:
            raise HTTPException(status_code=404, detail="Project not found")

        update_project = project.model_dump(exclude_unset = True)

        for field,value in update_project.items():
            setattr(project_id,field,value)

        await session.commit()
        await session.refresh(project_id)

        return project_id

@router.delete("/projects/{project_id}", response_model=ProjectResponse)
async def delete_project(project_id: int):
    async with SessionLocal() as session:
        project = await session.get(Projects, project_id)

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        await session.delete(project)
        await session.commit()

        return project
