from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Online",  "message": "Welcome to the DevOps Book API!", "version": "1.0.1"}

def test_create_book():
    book_data = {"id": 1, "title": "DevOps Handbook", "author": "Gene Kim", "published_year": 2016}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "DevOps Handbook"