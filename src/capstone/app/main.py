import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from . import models

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(employee_router)
app.include_router(project_router)
app.include_router(resource_router)
app.include_router(assignment_router)
