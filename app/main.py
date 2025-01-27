from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests
import os
from dotenv import load_dotenv

from app import models, database, schemas, crud

# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in the environment variables")

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL if different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to add a city to the predefined cities list
@app.post("/predefined_cities/", response_model=schemas.PredefinedCity)
async def add_predefined_city(city: schemas.PredefinedCityCreate, db: Session = Depends(get_db)):
    return crud.create_predefined_city(db=db, city=city)

# Endpoint to fetch weather for multiple predefined cities
@app.get("/weather/multiple", response_model=list[schemas.Weather])
async def get_weather_for_multiple_cities(db: Session = Depends(get_db)):
    predefined_cities = crud.get_predefined_cities(db=db)
    weather_data = []

    for city in predefined_cities:
        print(f"Fetching weather data for {city.city}")  # Add logging
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city.city}"
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()
            print(f"Weather data for {city.city}: {data}")  # Add logging
            weather = schemas.WeatherCreate(
                city=city.city,
                condition=data["current"]["condition"]["text"],
                temperature=data["current"]["temp_c"],
                icon_url=f"https:{data['current']['condition']['icon']}"  # Ensure the icon URL is complete
            )
            db_weather = crud.create_weather(db=db, weather=weather)
            weather_data.append(db_weather)
            print(f"Weather data for {city.city} added to the database")  # Add logging
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city.city}: {e}")
            weather_data.append({"city": city.city, "error": "Unable to fetch weather"})
        except KeyError as e:
            print(f"Error parsing data for {city.city}: {e}")
            weather_data.append({"city": city.city, "error": "Invalid response structure"})

    return weather_data

# Endpoint to fetch weather for a single city
@app.get("/weather/", response_model=schemas.Weather)
async def get_weather(city: str = Query(...), db: Session = Depends(get_db)):
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"

    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()
        weather = schemas.WeatherCreate(
            city=city,
            condition=data["current"]["condition"]["text"],
            temperature=data["current"]["temp_c"],
            icon_url=f"https:{data['current']['condition']['icon']}"  # Ensure the icon URL is complete
        )
        db_weather = crud.create_weather(db=db, weather=weather)
        return db_weather
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from WeatherAPI")
    except KeyError:
        raise HTTPException(status_code=404, detail="City not found in WeatherAPI data")

# Endpoint to list all weather data
@app.get("/weather/all", response_model=list[schemas.Weather])
async def get_all_weather(db: Session = Depends(get_db)):
    return crud.get_all_weather(db=db)

# Endpoint to clear all weather data
@app.delete("/weather/clear")
async def clear_weather_data(db: Session = Depends(get_db)):
    crud.delete_all_weather(db=db)
    return {"message": "All weather data cleared"}
