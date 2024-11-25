from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis

from app.api import router
from app.core.config import settings

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(docs_url="/swagger", lifespan=lifespan)
add_pagination(app)
app.include_router(router)
