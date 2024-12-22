Create .env file
OPENWEATHER_API_KEY=your_api_key_here

Install dependencies:
pip install -r requirements.txt

Run locally:
uvicorn app.main:app --reload

Run with Docker:
docker build -t weather-app .
docker run -p 8000:8000 weather-app

Testing Instructions:
pytest app/unit_tests.py

