import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_full_flow():
    # Test root
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    
    # Test weather fetch
    response = httpx.post(f"{BASE_URL}/weather/", json={"city": "Tokyo"})
    assert response.status_code == 200
    assert "main" in response.json()

    # Test adding and retrieving favorites
    httpx.post(f"{BASE_URL}/favorites/", json={"city": "Berlin"})
    favorites = httpx.get(f"{BASE_URL}/favorites/")
    assert favorites.status_code == 200
    assert len(favorites.json()) > 0
