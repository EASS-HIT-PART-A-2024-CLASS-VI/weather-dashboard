from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    condition = Column(String)
    temperature = Column(Float)
    icon_url = Column(String)

class PredefinedCity(Base):
    __tablename__ = "predefined_cities"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True, index=True)
