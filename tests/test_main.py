import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, send_email
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


def test_login_user(test_db):
    response = client.post("/token", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_create_subscription(test_db):
    response = client.post("/subscriptions/", json={"city": "Test City"}, headers={"Authorization": f"Bearer {get_access_token()}"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"

def test_get_subscriptions(test_db):
    response = client.get("/subscriptions/", headers={"Authorization": f"Bearer {get_access_token()}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_delete_subscription(test_db):
    response = client.post("/subscriptions/", json={"city": "Test City"}, headers={"Authorization": f"Bearer {get_access_token()}"})
    subscription_id = response.json()["id"]
    response = client.delete(f"/subscriptions/{subscription_id}", headers={"Authorization": f"Bearer {get_access_token()}"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"

@patch("app.main.send_email")
def test_send_notification(mock_send_email, test_db):
    mock_send_email.return_value = None
    response = client.post("/notifications/send", headers={"Authorization": f"Bearer {get_access_token()}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Notification sent"

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

def get_access_token():
    response = client.post("/token", data={"username": "test@example.com", "password": "testpassword"})
    return response.json()["access_token"]
