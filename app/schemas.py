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
        orm_mode = True
