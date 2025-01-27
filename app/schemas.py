from pydantic import BaseModel

class WeatherBase(BaseModel):
    city: str
    condition: str
    temperature: float
    icon_url: str

class WeatherCreate(WeatherBase):
    pass

class Weather(WeatherBase):
    id: int

    class Config:
        from_attributes = True

class PredefinedCityBase(BaseModel):
    city: str

class PredefinedCityCreate(PredefinedCityBase):
    pass

class PredefinedCity(PredefinedCityBase):
    id: int

    class Config:
        from_attributes = True
