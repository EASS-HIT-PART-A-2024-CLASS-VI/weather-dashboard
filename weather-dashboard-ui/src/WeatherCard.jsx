import React, { useState } from "react";
import "./display.css"; // Import the CSS file

const WeatherCard = ({ city, condition, temperature, icon, date, day, onDelete, subscriptionId, isDefault }) => {
  const [error, setError] = useState("");

  const handleDelete = () => {
    if (isDefault) {
      setError("You can't delete this city.");
    } else {
      console.log(`Deleting subscription with ID: ${subscriptionId}`);
      onDelete(subscriptionId);
    }
  };

  return (
    <div className={`weather-card ${isDefault ? "default-city" : ""}`}>
      <div className="weather-card-header">
        <h3>{city}</h3>
        {!isDefault && onDelete && (
          <button className="delete-button" onClick={handleDelete}>
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
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default WeatherCard;
