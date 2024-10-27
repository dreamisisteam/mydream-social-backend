from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import taskiq_fastapi

from config import get_settings, get_cache_settings
from database import init_db
from cache import get_cache
from broker import init_broker, taskiq_broker
from routers import (
    auth_api_router,
    users_api_router,
    recommendations_api_router,
)
from tasks.process_recommendations import process_users_info
from tasks.update_avatars import update_users_avatars

settings = get_settings()
cache = get_cache_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Цикл жизнедеятельности веб-приложения."""
    async with init_db(app):
        async with get_cache() as _cache:
            _app.state.cache = _cache

            async with init_broker():
                await process_users_info.kiq()
                await update_users_avatars.kiq()
                yield


app = FastAPI(
    lifespan=lifespan,
)

taskiq_fastapi.init(taskiq_broker, 'main:app')


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
router.include_router(recommendations_api_router, tags=['Recommendations'])

app.include_router(router)
