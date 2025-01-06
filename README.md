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

### Check if Docker Works
1. Ensure Docker is installed and running.
2. Navigate to the project root directory.
3. Run the following command to build and start the containers:
   ```
   docker-compose up --build
   ```
4. Open your browser and navigate to:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000

## Testing Instructions

### Backend Tests
Navigate to the project root directory and run:
```
pytest app/unit_tests.py
```

### Frontend Tests
Navigate to the `weather-dashboard-ui` directory and run:
```
npm test
```

