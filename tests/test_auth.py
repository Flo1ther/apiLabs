import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Login
print("=== LOGIN ===")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"user_id": "user123"}
)
print(login_response.json())

tokens = login_response.json()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]

# 2. Get Books
print("\n=== GET BOOKS ===")
books_response = requests.get(
    f"{BASE_URL}/api/books",
    headers={"Authorization": f"Bearer {access_token}"}
)
print(books_response.json())

# 3. Refresh Token
print("\n=== REFRESH TOKEN ===")
refresh_response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": refresh_token}
)
print(refresh_response.json())

# 4. Create Book
print("\n=== CREATE BOOK ===")
new_access_token = refresh_response.json()["access_token"]
create_response = requests.post(
    f"{BASE_URL}/api/books",
    json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "123-456",
        "pages": 300,
        "year": 2024
    },
    headers={"Authorization": f"Bearer {new_access_token}"}
)
print(create_response.json())