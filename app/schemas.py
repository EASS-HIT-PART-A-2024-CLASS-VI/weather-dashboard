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

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    subscriptions: list["Subscription"] = []

    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    city: str
    is_default: bool = False

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
