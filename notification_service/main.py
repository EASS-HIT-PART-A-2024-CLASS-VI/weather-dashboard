from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import requests

app = FastAPI()

class Notification(BaseModel):
    email: str

def send_email(email: str, message: str):
    msg = MIMEText(message)
    msg["Subject"] = "Weather Update"
    msg["From"] = "your-email@example.com"
    msg["To"] = email

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.login("your-email@example.com", "your-password")
        server.sendmail("your-email@example.com", email, msg.as_string())

@app.post("/notifications/send")
async def send_notification(notification: Notification, background_tasks: BackgroundTasks):
    response = requests.post("http://backend:8000/notifications/send", json={"user_email": notification.email})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    background_tasks.add_task(send_email, notification.email, response.json()["message"])
    return {"message": "Notification sent"}
