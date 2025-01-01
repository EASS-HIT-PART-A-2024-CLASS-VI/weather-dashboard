import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in the environment variables")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL if different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to fetch weather for multiple cities
@app.get("/weather/multiple")
async def get_weather_for_multiple_cities():
    cities = ["Haifa", "Paris", "London", "Madrid", "Berlin"]
    weather_data = []

    for city in cities:
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()
            weather_data.append({
                "city": city,
                "condition": data["current"]["condition"]["text"],
                "temperature": data["current"]["temp_c"],
                "iconUrl": data["current"]["condition"]["icon"]  # Extract icon code
            })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
            weather_data.append({"city": city, "error": "Unable to fetch weather"})
        except KeyError:
            print(f"Error parsing data for {city}")
            weather_data.append({"city": city, "error": "Invalid response structure"})

    return weather_data


# Endpoint to fetch weather for a single city
@app.get("/weather/")
async def get_weather(city: str = Query(...)):
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"

    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()

        return {
            "city": city,
            "condition": data["current"]["condition"]["text"],
            "temperature": data["current"]["temp_c"],
            "iconUrl": data["current"]["condition"]["icon"]  # Extract icon code
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from WeatherAPI")
    except KeyError:
        raise HTTPException(status_code=404, detail="City not found in WeatherAPI data")
