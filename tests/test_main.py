import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app import models

# Set up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL

# Create the test database
Base.metadata.create_all(bind=engine)

# Create a TestClient
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Create a new database session for testing
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_add_predefined_city(test_db):
    response = client.post("/predefined_cities/", json={"city": "Test City"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"

def test_get_weather_for_multiple_cities(test_db):
    response = client.get("/weather/multiple")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_weather(test_db):
    response = client.get("/weather/", params={"city": "Test City"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"

def test_get_all_weather(test_db):
    response = client.get("/weather/all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_clear_weather_data(test_db):
    response = client.delete("/weather/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All weather data cleared"
