from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    subscriptions = relationship("Subscription", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    is_default = Column(Boolean, default=False)
    user = relationship("User", back_populates="subscriptions")
