import logging
from fastapi import FastAPI
from datetime import datetime


from .routers.employee import router as employee_router
from .routers.project import router as project_router
from .routers.resource import router as resource_router
from .routers.assignment import router as assignment_router


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(employee_router)

app.include_router(project_router)

app.include_router(resource_router)

app.include_router(assignment_router)
