import React from "react";
import WeatherCard from "./WeatherCard";

const Display = ({ weatherData, searchedWeather, searchedCities, currentDate, currentTime }) => {
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
  );
};

export default Display;
