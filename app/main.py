from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List
import sqlite3
import os
import httpx

# Environment variable for API key
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = FastAPI(title="Weather Dashboard API")

# Database setup
def get_db():
    conn = sqlite3.connect("weather.db")
    conn.execute("CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY, city TEXT)")
    return conn

# Pydantic schemas
class CityRequest(BaseModel):
    city: str

class FavoriteCitiesResponse(BaseModel):
    id: int
    city: str

# Routes
@app.get("/")
def root():
    return {"message": "Welcome to the Weather Dashboard API"}

@app.post("/weather/")
async def get_weather(city: str = Query(...)):  # Use Query to define it as a query parameter
    available_cities = {"paris": "Sunny", "london": "Rainy"}  # Example mock data
    if city.lower() not in available_cities:
        raise HTTPException(status_code=404, detail="City not found")
    return {"city": city, "weather": available_cities[city.lower()]}

@app.post("/favorites/")
def add_favorite_city(data: CityRequest, db=Depends(get_db)):
    db.execute("INSERT INTO favorites (city) VALUES (?)", (data.city,))
    db.commit()
    return {"message": f"{data.city} added to favorites"}

@app.get("/favorites/", response_model=List[FavoriteCitiesResponse])
def get_favorite_cities(db=Depends(get_db)):
    cursor = db.execute("SELECT id, city FROM favorites")
    cities = cursor.fetchall()
    return [{"id": row[0], "city": row[1]} for row in cities]
