from fastapi import Request, HTTPException, status
from redis.exceptions import RedisError


EXCLUDED_PATHS = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
    "/books",
]


class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def check(self, request: Request):
        path = request.url.path

        if path in EXCLUDED_PATHS:
            return

        if not self.redis:
            return

        auth_header = request.headers.get("Authorization")

        if auth_header:
            limit = 10
            key = f"rate_limit:user:{auth_header}"
        else:
            limit = 2
            client_ip = request.client.host if request.client else "anonymous"
            key = f"rate_limit:anonymous:{client_ip}"

        try:
            current = await self.redis.incr(key)

            if current == 1:
                await self.redis.expire(key, 60)

        except RedisError:
            return

        if current > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )