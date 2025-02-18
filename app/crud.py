from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

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

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate, user_id: int):
    db_subscription = models.Subscription(**subscription.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscriptions_by_user(db: Session, user_id: int):
    subscriptions = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).all()
    logger.info(f"User ID {user_id} has subscriptions: {subscriptions}")
    return subscriptions

def get_default_subscriptions(db: Session):
    return db.query(models.Subscription).filter(models.Subscription.is_default == True).all()
