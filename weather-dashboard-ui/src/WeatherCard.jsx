import React from "react";
import "./display.css"; // Import the CSS file

const WeatherCard = ({ city, condition, temperature, icon, date, day }) => {
  return (
    <div className="weather-card">
      <h3>{city}</h3>
      <p className="weather-condition">{condition}</p>
      <img src={icon} alt={condition} className="weather-icon" />
      <p className="weather-temperature">{temperature}°C</p>
      <div className="weather-date-container">
        <p className="weather-date">{date}</p>
        <p className="weather-day">{day}</p>
      </div>
    </div>
  );
};

export default WeatherCard;
