import React from "react";
import "./display.css"; // Import the CSS file

const WeatherCard = ({ city, condition, temperature, icon, date, day, onDelete, subscriptionId, isDefault }) => {
  return (
    <div className="weather-card">
      <div className="weather-card-header">
        <h3>{city}</h3>
        {!isDefault && subscriptionId && onDelete && (
          <button
            className="delete-button"
            onClick={() => {
              console.log(`Deleting subscription with ID: ${subscriptionId}`);
              onDelete(subscriptionId);
            }}
          >
            X
          </button>
        )}
      </div>
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
