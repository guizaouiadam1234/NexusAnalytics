import json
import time
import importlib
from typing import Any

from app.core.config import settings

try:
    redis_asyncio = importlib.import_module("redis.asyncio")
    Redis = getattr(redis_asyncio, "Redis", None)
except Exception:
    Redis = None


class CacheClient:
    def __init__(self) -> None:
        self._redis = None
        self._memory_cache: dict[str, tuple[float, Any]] = {}

        if Redis is not None and settings.redis_url:
            try:
                self._redis = Redis.from_url(settings.redis_url, decode_responses=True)
            except Exception:
                self._redis = None

    async def get_json(self, key: str) -> Any | None:
        if self._redis is not None:
            try:
                raw_value = await self._redis.get(key)
                if raw_value is None:
                    return None
                return json.loads(raw_value)
            except Exception:
                return None

        memory_entry = self._memory_cache.get(key)
        if memory_entry is None:
            return None

        expires_at, value = memory_entry
        if expires_at < time.time():
            self._memory_cache.pop(key, None)
            return None

        return value

    async def set_json(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        effective_ttl = ttl_seconds or settings.cache_ttl_seconds

        if self._redis is not None:
            try:
                await self._redis.set(key, json.dumps(value), ex=effective_ttl)
                return
            except Exception:
                pass

        self._memory_cache[key] = (time.time() + effective_ttl, value)


cache_client = CacheClient()
