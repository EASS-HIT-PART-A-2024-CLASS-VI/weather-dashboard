from sqlalchemy.orm import Session
from . import models, schemas

def create_weather(db: Session, weather: schemas.WeatherCreate):
    db_weather = models.Weather(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def get_all_weather(db: Session):
    return db.query(models.Weather).all()

def delete_all_weather(db: Session):
    db.query(models.Weather).delete()
    db.commit()

def create_predefined_city(db: Session, city: schemas.PredefinedCityCreate):
    db_city = models.PredefinedCity(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_predefined_cities(db: Session):
    return db.query(models.PredefinedCity).all()
