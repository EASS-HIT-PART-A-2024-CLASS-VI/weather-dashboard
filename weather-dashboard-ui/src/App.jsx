import React, { useState, useEffect } from "react";
import { getWeatherForMultipleCities, getWeather } from "./api";

function App() {
  const [weatherData, setWeatherData] = useState([]);
  const [searchCity, setSearchCity] = useState("");
  const [searchedWeather, setSearchedWeather] = useState(null);

  // Fetch weather data for predefined cities on component mount
  useEffect(() => {
    async function fetchWeatherData() {
      try {
        const data = await getWeatherForMultipleCities();
        setWeatherData(data);
      } catch (error) {
        console.error("Error fetching weather data for multiple cities:", error);
      }
    }
    fetchWeatherData();
  }, []);

  // Handle search for a specific city
  const handleSearch = async () => {
    if (!searchCity.trim()) return;
    try {
      const data = await getWeather(searchCity.trim());
      setSearchedWeather(data);
    } catch (error) {
      console.error("Error fetching weather for the searched city:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Weather Dashboard</h1>

      {/* Display predefined cities' weather */}
      <h2>Weather in Predefined Cities:</h2>
      <ul>
        {weatherData.map((weather, index) => (
          <li key={index}>
            {weather.city}: {weather.condition}, {weather.temperature}°C
          </li>
        ))}
      </ul>

      {/* Search for a city */}
      <h2>Search for a City:</h2>
      <input
        type="text"
        value={searchCity}
        onChange={(e) => setSearchCity(e.target.value)}
        placeholder="Enter city name"
      />
      <button onClick={handleSearch}>Search</button>

      {/* Display weather for the searched city */}
      {searchedWeather && (
        <div>
          <h3>Weather in {searchedWeather.city}:</h3>
          <p>
            {searchedWeather.condition}, {searchedWeather.temperature}°C
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
