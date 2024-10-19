from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database import init_db
from cache import get_cache
from routers import (
    auth_api_router,
    users_api_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Цикл жизнедеятельности веб-приложения."""
    _app.cache = get_cache()

    async with init_db(app):
        yield

    await _app.cache.close()


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

router = APIRouter(
    prefix=settings.BASE_API_PREFIX,
)
router.include_router(auth_api_router, tags=['Authentication'])
router.include_router(users_api_router, tags=['User'])

app.include_router(router)
