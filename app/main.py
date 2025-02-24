import logging
from fastapi import FastAPI, HTTPException, Query, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
import smtplib
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import models, database, schemas, crud

# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in the environment variables")

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL if different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# Endpoint to register a new user
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    return crud.create_user(db=db, user=user)

# Endpoint to login a user
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(background_tasks: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Fetch weather data for user's subscribed cities
    subscriptions = crud.get_subscriptions_by_user(db=db, user_id=user.id)
    message = f"Hello {user.email},\n\nYou have successfully logged in to the Weather Dashboard.\n\nWeather updates for your subscribed cities:\n"
    for subscription in subscriptions:
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={subscription.city}"
        response = requests.get(weather_url)
        data = response.json()
        message += f"{subscription.city}: {data['current']['condition']['text']}, {data['current']['temp_c']}°C\n"
    
    logger.info(f"Sending login notification email to {user.email}")
    background_tasks.add_task(send_email, user.email, message)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to create a subscription for a user
@app.post("/subscriptions/", response_model=schemas.Subscription)
async def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_subscription(db=db, subscription=subscription, user_id=current_user.id)

# Endpoint to get subscriptions for a user
@app.get("/subscriptions/", response_model=list[schemas.Subscription])
async def get_subscriptions(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_subscriptions_by_user(db=db, user_id=current_user.id)

# Endpoint to delete a subscription for a user
@app.delete("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    logger.info(f"Attempting to delete subscription with ID: {subscription_id} for user ID: {current_user.id}")
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id, models.Subscription.user_id == current_user.id).first()
    logger.info(f"Query result: {subscription}")
    if not subscription:
        logger.info(f"Subscription with ID: {subscription_id} not found for user ID: {current_user.id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    logger.info(f"Found subscription: {subscription}")
    db.delete(subscription)
    db.commit()
    logger.info(f"Subscription with ID: {subscription_id} deleted for user ID: {current_user.id}")
    return subscription

# Endpoint to send notifications to a user
@app.post("/notifications/send")
async def send_notification(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    subscriptions = crud.get_subscriptions_by_user(db=db, user_id=current_user.id)
    message = "Weather updates for your subscribed cities:\n"
    for subscription in subscriptions:
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={subscription.city}"
        response = requests.get(weather_url)
        data = response.json()
        message += f"{subscription.city}: {data['current']['condition']['text']}, {data['current']['temp_c']}°C\n"
    logger.info(f"Sending weather notification email to {current_user.email}")
    background_tasks.add_task(send_email, current_user.email, message)
    return {"message": "Notification sent"}

def send_email(email: str, message: str):
    logger.info(f"Attempting to send email to {email}")
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Weather Update"
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = email

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
            server.sendmail(os.getenv("SMTP_USER"), email, msg.as_string())
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")

# Initialize default cities
def initialize_default_cities(db: Session):
    default_cities = ["Tokyo", "Berlin", "Miami", "Jerusalem"]
    for city in default_cities:
        if not db.query(models.Subscription).filter(models.Subscription.city == city, models.Subscription.is_default == True).first():
            db_subscription = models.Subscription(city=city, is_default=True, user_id=None)
            db.add(db_subscription)
            db.commit()

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    initialize_default_cities(db)

# Endpoint to fetch weather for multiple predefined cities
@app.get("/weather/multiple", response_model=list[schemas.Weather])
async def get_weather_for_multiple_cities(db: Session = Depends(get_db)):
    subscriptions = crud.get_default_subscriptions(db=db)
    weather_data = []

    for subscription in subscriptions:
        logger.info(f"Fetching weather data for {subscription.city}")  # Add logging
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={subscription.city}"
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Weather data for {subscription.city}: {data}")  # Add logging
            weather = schemas.WeatherCreate(
                city=subscription.city,
                condition=data["current"]["condition"]["text"],
                temperature=data["current"]["temp_c"],
                icon_url=f"https:{data['current']['condition']['icon']}"  # Ensure the icon URL is complete
            )
            db_weather = crud.create_weather(db=db, weather=weather)
            weather_data.append({
                "id": db_weather.id,
                "city": db_weather.city,
                "condition": db_weather.condition,
                "temperature": db_weather.temperature,
                "icon_url": db_weather.icon_url,
                "isDefault": subscription.is_default
            })
            logger.info(f"Weather data for {subscription.city} added to the database")  # Add logging
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {subscription.city}: {e}")
            weather_data.append({"city": subscription.city, "error": "Unable to fetch weather", "isDefault": subscription.is_default})
        except KeyError as e:
            logger.error(f"Error parsing data for {subscription.city}: {e}")
            weather_data.append({"city": subscription.city, "error": "Invalid response structure", "isDefault": subscription.is_default})

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
        logger.error(f"Error fetching weather for {city}: {e}")
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
