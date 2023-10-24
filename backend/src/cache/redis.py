import json
from typing import Any

from aioredis import Redis, from_url

import main
from core.config import settings
from helpers.datetime import DateTimeWorker as dtw


async def init_redis() -> Redis:
    """Initialize Redis client."""
    return from_url(str(settings.REDIS_URL))


async def set_cache(key: str, data: Any, expire_time_seconds: int) -> None:
    """Sets the value by key in the cache before time expires."""
    await main.app.state.redis.set(
        key,
        json.dumps(data, default=dtw.serialize_dates),
        expire_time_seconds
    )


async def get_cache(key: str) -> Any:
    """Gets a value from the cache by key."""
    cached_data = await main.app.state.redis.get(key)

    if cached_data:
        return json.loads(cached_data, object_hook=dtw.datetime_parser)
