const API_BASE_URL = "http://127.0.0.1:8000"; // Backend URL

// Fetch weather for multiple predefined cities
export async function getWeatherForMultipleCities() {
  const response = await fetch(`${API_BASE_URL}/weather/multiple`);
  if (!response.ok) {
    throw new Error("Failed to fetch weather for multiple cities");
  }
  return response.json();
}

// Fetch weather for a specific city
export async function getWeather(city) {
  const response = await fetch(`${API_BASE_URL}/weather/?city=${city}`);
  if (!response.ok) {
    throw new Error("Failed to fetch weather for the city");
  }
  return response.json();
}
