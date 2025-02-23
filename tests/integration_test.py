import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, send_email
from app.database import SessionLocal, Base, engine
from app import models, crud

# Set up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
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

@patch("app.main.send_email")
def test_full_flow(mock_send_email, test_db):
    mock_send_email.return_value = None

    # Ensure the user does not already exist
    existing_user = crud.get_user_by_email(test_db, email="fintegration@example.com")
    if existing_user:
        test_db.delete(existing_user)
        test_db.commit()

    # Register a new user
    response = client.post("/users/", json={"email": "fintegration@example.com", "password": "integrationpassword"})
    print("Response status code:", response.status_code)
    print("Response content:", response.content)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "fintegration@example.com"

    # Login the user
    response = client.post("/token", data={"username": "fintegration@example.com", "password": "integrationpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a subscription
    response = client.post("/subscriptions/", json={"city": "Integration City"}, headers=headers)
    assert response.status_code == 200
    subscription_id = response.json()["id"]

    # Get subscriptions
    response = client.get("/subscriptions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    # Send notification
    response = client.post("/notifications/send", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Notification sent"

    # Get weather for multiple cities
    response = client.get("/weather/multiple")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Get weather for a single city
    response = client.get("/weather/", params={"city": "Integration City"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Integration City"

    # Get all weather data
    response = client.get("/weather/all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Clear weather data
    response = client.delete("/weather/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All weather data cleared"

    # Delete the subscription
    response = client.delete(f"/subscriptions/{subscription_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Integration City"
