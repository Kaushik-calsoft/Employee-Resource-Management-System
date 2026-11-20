from fastapi import FastAPI
from .routers.employee import router as employee_router
from .routers.project import router as project_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(employee_router)

app.include_router(project_router)



