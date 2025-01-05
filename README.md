# Weather Dashboard

## Setup

### Create .env file
```
WEATHER_API_KEY=your_api_key_here
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run Backend Locally
```
uvicorn app.main:app --reload
```

### Run Frontend Locally
Navigate to the `weather-dashboard-ui` directory and run:
```
npm install
npm start
```

## Run with Docker

### Build and Run Containers
```
docker-compose up --build
```

### Access the Application
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Testing Instructions

### Backend Tests
```
pytest app/unit_tests.py
```

### Frontend Tests
Navigate to the `weather-dashboard-ui` directory and run:
```
npm test
```

