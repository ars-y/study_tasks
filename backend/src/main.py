from contextlib import asynccontextmanager
from typing import Generator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from cache.redis import init_redis
from core.constants import PERIOD_DAYS, SECONDS_PER_DAY
from jobs import parsing
from routers.spimex import router as spimex_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    """Lifespan for redis client and job schedulers."""
    app.state.redis = await init_redis()

    schedulers = AsyncIOScheduler()
    schedulers.add_job(
        parsing.run,
        'interval',
        seconds=PERIOD_DAYS*SECONDS_PER_DAY
    )
    schedulers.start()

    yield

    schedulers.shutdown()

    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(spimex_router, prefix='/spimex')
