from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "description": "Test",
            "status": "available",
            "year": 2020
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_book():
    create = client.post(
        "/books/",
        json={
            "title": "Delete Book",
            "author": "Author",
            "description": "Test",
            "status": "available",
            "year": 2022
        }
    )

    book_id = create.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204
