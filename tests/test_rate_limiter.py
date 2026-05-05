import pytest
from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport

from services.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_anonymous_user_not_reached_limit(app_with_test_db):
    mock_redis = AsyncMock()
    mock_redis.incr.return_value = 1
    mock_redis.expire.return_value = True

    app_with_test_db.state.rate_limiter = RateLimiter(mock_redis)

    transport = ASGITransport(app=app_with_test_db)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_anonymous_user_reached_limit(app_with_test_db):
    mock_redis = AsyncMock()
    mock_redis.incr.return_value = 3
    mock_redis.expire.return_value = True

    app_with_test_db.state.rate_limiter = RateLimiter(mock_redis)

    transport = ASGITransport(app=app_with_test_db)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books")

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"


@pytest.mark.asyncio
async def test_authorized_user_not_reached_limit(app_with_test_db):
    mock_redis = AsyncMock()
    mock_redis.incr.return_value = 10
    mock_redis.expire.return_value = True

    app_with_test_db.state.rate_limiter = RateLimiter(mock_redis)

    transport = ASGITransport(app=app_with_test_db)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/books",
            headers={"Authorization": "Bearer test-token"},
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_authorized_user_reached_limit(app_with_test_db):
    mock_redis = AsyncMock()
    mock_redis.incr.return_value = 11
    mock_redis.expire.return_value = True

    app_with_test_db.state.rate_limiter = RateLimiter(mock_redis)

    transport = ASGITransport(app=app_with_test_db)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/books",
            headers={"Authorization": "Bearer test-token"},
        )

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"