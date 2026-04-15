import pytest
from httpx import AsyncClient
from httpx import ASGITransport


@pytest.mark.asyncio
async def test_create_book(app_with_test_db):
    transport = ASGITransport(app=app_with_test_db)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/books",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "status": "available",
                "year": 2024,
                "description": "Test Description"
            }
        )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"


@pytest.mark.asyncio
async def test_get_books(app_with_test_db):
    transport = ASGITransport(app=app_with_test_db)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create a book first
        await ac.post(
            "/books",
            json={
                "title": "Test Book 1",
                "author": "Test Author",
                "status": "available",
                "year": 2024,
                "description": "Test Description 1"
            }
        )

        # Get books with cursor pagination
        response = await ac.get("/books?limit=10")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)
    assert "cursor" in data
    assert "has_more" in data