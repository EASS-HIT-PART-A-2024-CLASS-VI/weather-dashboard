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

// Add a city to the predefined cities list
export async function addPredefinedCity(city) {
  const response = await fetch(`${API_BASE_URL}/predefined_cities/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ city }),
  });
  if (!response.ok) {
    throw new Error("Failed to add predefined city");
  }
  return response.json();
}

// Register a new user
export async function registerUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error("Failed to register user");
  }
  return response.json();
}

// Login a user
export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ username: email, password }),
  });
  if (!response.ok) {
    throw new Error("Failed to login");
  }
  return response.json();
}

// Create a subscription for a user
export async function createSubscription(token, city) {
  const response = await fetch(`${API_BASE_URL}/subscriptions/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ city }),
  });
  if (!response.ok) {
    throw new Error("Failed to create subscription");
  }
  return response.json();
}

// Fetch subscriptions for a user
export async function getSubscriptions(token) {
  const response = await fetch(`${API_BASE_URL}/subscriptions/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch subscriptions");
  }
  return response.json();
}

// Delete a subscription for a user
export async function deleteSubscription(token, subscriptionId) {
  const response = await fetch(`${API_BASE_URL}/subscriptions/${subscriptionId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to delete subscription");
  }
  return response.json();
}

// Send OTP to a user
export async function sendOtp(email) {
  const response = await fetch(`${API_BASE_URL}/send-otp/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  });
  if (!response.ok) {
    throw new Error("Failed to send OTP");
  }
  return response.json();
}
