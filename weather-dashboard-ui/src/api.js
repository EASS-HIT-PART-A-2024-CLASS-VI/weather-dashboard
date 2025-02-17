import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const getWeatherForMultipleCities = async () => {
  const response = await axios.get(`${API_URL}/weather/multiple`);
  return response.data;
};

export const getWeather = async (city) => {
  const response = await axios.get(`${API_URL}/weather`, { params: { city } });
  return response.data;
};

export const registerUser = async (email, password) => {
  const response = await axios.post(`${API_URL}/users/`, { email, password });
  return response.data;
};

export const loginUser = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/token`, new URLSearchParams({
      username: email,
      password: password
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

export const createSubscription = async (token, city) => {
  const response = await axios.post(
    `${API_URL}/subscriptions/`,
    { city },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

export const getSubscriptions = async (token) => {
  const response = await axios.get(`${API_URL}/subscriptions/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const deleteSubscription = async (token, subscriptionId) => {
  const response = await axios.delete(`${API_URL}/subscriptions/${subscriptionId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getDefaultSubscriptions = async () => {
  const response = await axios.get(`${API_URL}/subscriptions/default`);
  return response.data;
};
