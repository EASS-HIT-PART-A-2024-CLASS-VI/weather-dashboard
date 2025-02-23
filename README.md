# Weather Dashboard

Welcome to the Weather Dashboard project! This project allows you to view weather information for multiple cities, register and log in users, and manage city subscriptions. The application is built using React for the frontend, FastAPI for the backend, SQLite for data storage, and Docker for containerization.

## Project Explanation Video

Watch the video below for a detailed explanation of the project:

[![Weather Dashboard Project Explanation](https://img.youtube.com/vi/XvtxC01EsYk/0.jpg)](https://youtu.be/XvtxC01EsYk)

## Prerequisites

Before you begin, make sure you have the following installed:

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/fastap.git
   cd fastap
   ```

2. **Set up environment variables**:

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   WEATHER_API_KEY=your-weather-api-key
   SECRET_KEY=your-secret-key
   ```

3. **Build and run the Docker containers**:

   ```bash
   docker-compose up --build
   ```

   This will build and start the backend, frontend, and notification services.

4. **Access the application**:

   - Frontend: Open your browser and go to `http://localhost:3000`
   - Backend API: The backend API is running at `http://localhost:8000`
   - Notification Service: The notification service is running at `http://localhost:8001`

## Features

- **Weather Information**: View weather information for multiple predefined cities.
- **User Registration and Login**: Register and log in users.
- **City Subscriptions**: Subscribe to cities to receive weather updates.
- **Notifications**: Send weather updates to subscribed users via email.

## Project Structure

Here's a quick overview of the project structure:

```
fastap/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
├── notification_service/
│   ├── Dockerfile
│   ├── main.py
├── weather-dashboard-ui/
│   ├── Dockerfile
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── index.js
│   │   ├── setupTests.js
├── Dockerfile
├── docker-compose.yml
├── .env
```

## Running Tests

To run the tests, use the following command:

```bash
pytest /c:/Users/afekd/fastap/tests
```

## Resetting the Database

To reset the database, delete the `weather.db` file from the project directory. This will remove all the data in your SQLite database, and a new empty database will be created the next time you run your application.

```bash
rm weather.db
```

After deleting the `weather.db` file, restart the application to create a new empty database.
