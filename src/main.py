from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from config import get_settings
from database import init_db
from routers import (
    auth_api_router,
    users_api_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Цикл жизнедеятельности веб-приложения."""
    async with init_db(app):
        yield


app = FastAPI(
    lifespan=lifespan,
)

router = APIRouter(
    prefix=settings.BASE_API_PREFIX,
)
router.include_router(auth_api_router, tags=['Authentication'])
router.include_router(users_api_router, tags=['User'])

app.include_router(router)
