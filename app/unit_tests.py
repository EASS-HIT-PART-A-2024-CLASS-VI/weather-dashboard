from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Weather Dashboard API"}

def test_get_weather():
    response = client.post("/weather/", json={"city": "London"})
    assert response.status_code == 200
    assert "main" in response.json()

def test_add_favorite():
    response = client.post("/favorites/", json={"city": "Paris"})
    assert response.status_code == 200
    assert response.json()["message"] == "Paris added to favorites"

def test_get_favorites():
    response = client.get("/favorites/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
