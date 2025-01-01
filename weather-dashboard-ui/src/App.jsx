import React, { useState, useEffect } from "react";
import { getWeatherForMultipleCities, getWeather } from "./api";
import "./display.css"; // Include the CSS file
import Display from "./display";

function App() {
  const [weatherData, setWeatherData] = useState([]);
  const [searchCity, setSearchCity] = useState("");
  const [searchedCities, setSearchedCities] = useState([]);

  const currentDate = new Date().toLocaleDateString();
  const currentTime = new Date().toLocaleTimeString();

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
      setSearchedCities((prevCities) => [...prevCities, data]); // Add the new city to the list
    } catch (error) {
      console.error("Error fetching weather for the searched city:", error);
    }
  };

  return (
    <div className="app-container">
      <h1>Weather Dashboard</h1>

      {/* Search for a city */}
      <h2>Search for a City:</h2>
      <div className="search-container">
        <input
          type="text"
          value={searchCity}
          onChange={(e) => setSearchCity(e.target.value)}
          placeholder="Enter city name"
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">
          Search
        </button>
      </div>

      {/* Display weather data */}
      <Display
        weatherData={weatherData}
        searchedCities={searchedCities}
      />
    </div>
  );
}

export default App;
