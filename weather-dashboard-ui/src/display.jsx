import React from "react";
import WeatherCard from "./WeatherCard";

const Display = ({ weatherData, searchedWeather, searchedCities }) => {
  const currentDate = new Date().toLocaleDateString();
  const currentTime = new Date().toLocaleTimeString();

  return (
    <div>
      {/* Display predefined cities' weather */}
      <div className="weather-cards-container">
        {weatherData.map((weather, index) => (
          <WeatherCard
            key={index}
            city={weather.city}
            condition={weather.condition}
            temperature={weather.temperature}
            icon={weather.iconUrl ? `${weather.iconUrl}` : ""}
            date={currentDate}
            day={currentTime}
          />
        ))}
      </div>

      {/* Display weather for the searched cities */}
      {searchedCities.length > 0 && (
        <div className="searched-weather">
          <h3>Weather in:</h3>
          <div className="searched-cities">
            {searchedCities.map((cityWeather, index) => (
              <WeatherCard
                key={index}
                city={cityWeather.city}
                condition={cityWeather.condition}
                temperature={cityWeather.temperature}
                icon={cityWeather.iconUrl ? `${cityWeather.iconUrl}` : ""}
                date={currentDate}
                day={currentTime}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Display;
