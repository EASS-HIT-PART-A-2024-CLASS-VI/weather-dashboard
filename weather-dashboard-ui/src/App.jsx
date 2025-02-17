import React, { useState, useEffect } from "react";
import { getWeatherForMultipleCities, getWeather, registerUser, loginUser, createSubscription, getSubscriptions, deleteSubscription, getDefaultSubscriptions } from "./api";
import "./display.css"; // Include the CSS file
import Display from "./display";
import SearchCity from "./components/SearchCity"; // Import the new SearchCity component
import WeatherCard from "./WeatherCard"; // Import the WeatherCard component

function App() {
  const [weatherData, setWeatherData] = useState([]);
  const [searchedWeather, setSearchedWeather] = useState(null);
  const currentDate = new Date().toLocaleDateString();
  const currentTime = new Date().toLocaleTimeString();
  const [city, setCity] = useState('');
  const [registerEmail, setRegisterEmail] = useState(''); // Separate state for Register email
  const [registerPassword, setRegisterPassword] = useState(''); // Separate state for Register password
  const [loginEmail, setLoginEmail] = useState(''); // Separate state for Login email
  const [loginPassword, setLoginPassword] = useState(''); // Separate state for Login password
  const [token, setToken] = useState('');
  const [loggedInEmail, setLoggedInEmail] = useState(''); // State to store logged-in user's email
  const [error, setError] = useState('');
  const [subscriptions, setSubscriptions] = useState([]);
  const [defaultSubscriptions, setDefaultSubscriptions] = useState([]); // State for default subscriptions

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

  // Fetch default subscriptions on component mount
  useEffect(() => {
    async function fetchDefaultSubscriptions() {
      try {
        const data = await getDefaultSubscriptions();
        setDefaultSubscriptions(data);
      } catch (error) {
        console.error("Error fetching default subscriptions:", error);
      }
    }
    fetchDefaultSubscriptions();
  }, []);

  // Handle search for a specific city
  const [searchedCities, setSearchedCities] = useState([]);

  const handleSearch = async (searchCity) => {
    try {
      const data = await getWeather(searchCity);
      setSearchedWeather(data);
  
      // Add the new searched city to the list
      setSearchedCities((prevCities) => [
        ...prevCities,
        {
          city: data.city,
          condition: data.condition,
          temperature: data.temperature,
          icon_url: data.icon_url,  // Ensure the icon URL is passed correctly
        },
      ]);
    } catch (error) {
      console.error("Error fetching weather for the searched city:", error);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerUser(registerEmail, registerPassword);
      setRegisterEmail('');
      setRegisterPassword('');
      setError('');
      alert('User registered successfully');
    } catch (err) {
      setError('Failed to register user');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear the error state before attempting to log in
    try {
      const data = await loginUser(loginEmail, loginPassword);
      setToken(data.access_token);
      setLoggedInEmail(loginEmail); // Store the logged-in user's email
      setLoginEmail('');
      setLoginPassword('');
      setError('');
      alert('User logged in successfully');
      fetchSubscriptions(data.access_token); // Fetch subscriptions after login
    } catch (err) {
      console.error("Error logging in:", err);
      setError('Failed to login');
    }
  };

  const handleSubscribe = async (e) => {
    e.preventDefault();
    try {
      await createSubscription(token, city);
      setCity('');
      setError('');
      alert('Subscription created successfully');
      fetchSubscriptions(token); // Fetch subscriptions after creating one
    } catch (err) {
      setError('Failed to create subscription');
    }
  };

  const handleDeleteSubscription = async (subscriptionId) => {
    console.log(`Attempting to delete subscription with ID: ${subscriptionId}`);
    try {
      await deleteSubscription(token, subscriptionId);
      setSubscriptions((prevSubscriptions) => prevSubscriptions.filter(sub => sub.id !== subscriptionId));
      setWeatherData((prevWeatherData) => prevWeatherData.filter(weather => weather.subscriptionId !== subscriptionId));
      alert('Subscription deleted successfully');
    } catch (err) {
      setError('Failed to delete subscription');
    }
  };

  const fetchSubscriptions = async (token) => {
    try {
      const data = await getSubscriptions(token);
      setSubscriptions(data);

      // Fetch weather data for each subscribed city
      const weatherPromises = data.map(async (subscription) => {
        try {
          const weatherData = await getWeather(subscription.city);
          return { ...weatherData, subscriptionId: subscription.id, isDefault: subscription.is_default }; // Include the subscription ID and isDefault flag
        } catch (error) {
          console.error(`Error fetching weather for ${subscription.city}:`, error);
          return { city: subscription.city, error: "Unable to fetch weather", subscriptionId: subscription.id, isDefault: subscription.is_default };
        }
      });

      const weatherResults = await Promise.all(weatherPromises);
      setWeatherData((prevWeatherData) => [...prevWeatherData, ...weatherResults]);
    } catch (err) {
      setError('Failed to fetch subscriptions');
    }
  };

  return (
    <div className="app-container">
      <h1>Weather Dashboard</h1>

      {/* Display logged-in user's email */}
      {loggedInEmail && <p>Logged in as {loggedInEmail}</p>}

      {/* Display default cities' weather */}
      <h2>Default Cities:</h2>
      <div className="weather-cards-container">
        {defaultSubscriptions.map((subscription) => (
          <WeatherCard
            key={subscription.id}
            city={subscription.city}
            condition={subscription.condition}
            temperature={subscription.temperature}
            icon={subscription.icon_url}
            date={currentDate}
            day={currentTime}
            isDefault={true}
          />
        ))}
      </div>

      {/* Display user-subscribed cities' weather */}
      <h2>Subscribed Cities:</h2>
      <Display weatherData={weatherData} searchedWeather={searchedWeather} searchedCities={searchedCities} currentDate={currentDate} currentTime={currentTime} onDelete={handleDeleteSubscription} />

      {/* Search for a city */}
      <h2>Search for a City:</h2>
      <SearchCity onSearch={handleSearch} />

      {/* Register user */}
      <h2>Register User:</h2>
      <form onSubmit={handleRegister} className="search-container">
        <input
          type="email"
          value={registerEmail}
          onChange={(e) => setRegisterEmail(e.target.value)}
          placeholder="Enter email"
          className="search-input"
        />
        <input
          type="password"
          value={registerPassword}
          onChange={(e) => setRegisterPassword(e.target.value)}
          placeholder="Enter password"
          className="search-input"
        />
        <button type="submit" className="search-button">Register</button>
      </form>

      {/* Login user */}
      <h2>Login User:</h2>
      <form onSubmit={handleLogin} className="search-container">
        <input
          type="email"
          value={loginEmail}
          onChange={(e) => setLoginEmail(e.target.value)}
          placeholder="Enter email"
          className="search-input"
        />
        <input
          type="password"
          value={loginPassword}
          onChange={(e) => setLoginPassword(e.target.value)}
          placeholder="Enter password"
          className="search-input"
        />
        <button type="submit" className="search-button">Login</button>
      </form>

      {/* Subscribe to city */}
      <h2>Subscribe to City:</h2>
      <form onSubmit={handleSubscribe} className="search-container">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          className="search-input"
        />
        <button type="submit" className="search-button">Subscribe</button>
      </form>

      {/* Display error message */}
      {error && <p className="error-message">{error}</p>}

      {/* Display subscribed cities */}
      <h2>Subscribed Cities:</h2>
      <div className="subscriptions-container">
        {subscriptions.map((subscription) => (
          <div key={subscription.id} className={`subscription-item ${subscription.is_default ? "default-city" : ""}`}>
            {subscription.city}
            {!subscription.is_default && (
              <button onClick={() => handleDeleteSubscription(subscription.id)}>Delete</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
