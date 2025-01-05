from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Weather Dashboard API"}

def test_get_weather():
    response = client.get("/weather/", params={"city": "London"})
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "condition" in data
    assert "temperature" in data
    assert "iconUrl" in data

def test_get_weather_for_multiple_cities():
    response = client.get("/weather/multiple")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for city_weather in data:
        assert "city" in city_weather
        assert "condition" in city_weather
        assert "temperature" in city_weather
        assert "iconUrl" in city_weather
