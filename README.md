# Weather Dashboard

This project is a weather dashboard application built with FastAPI for the backend and React for the frontend. It allows users to fetch weather data for multiple predefined cities and add new cities to the predefined list.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/weather-dashboard.git
   cd weather-dashboard
   ```

2. Create a `.env` file in the root directory and add your Weather API key:

   ```env
   WEATHER_API_KEY=your_weather_api_key_here
   ```

## Running the Application

1. Build and run the Docker containers:

   ```sh
   docker-compose up --build
   ```

2. The backend will be available at `http://localhost:8000`.
3. The frontend will be available at `http://localhost:3001`.

## API Endpoints

- `GET /weather/multiple`: Fetch weather data for multiple predefined cities.
- `GET /weather/`: Fetch weather data for a specific city.
- `POST /predefined_cities/`: Add a city to the predefined cities list.
- `GET /weather/all`: List all weather data.
- `DELETE /weather/clear`: Clear all weather data.

## Frontend

The frontend is a React application that allows users to:

- Search for weather data for a specific city.
- Add a city to the predefined cities list.
- View weather data for predefined cities.

## Viewing the SQLite Database

The application uses SQLite as the database. The database file is named `weather.db` and is located in the `/app` directory inside the Docker container.

To view the data inside the SQLite database, you can use one of the following methods:

### Option 1: SQLite Browser

1. Download and install [DB Browser for SQLite](https://sqlitebrowser.org/).
2. Open the application and open the `weather.db` file located in the `/app` directory of the Docker container.

### Option 2: SQLite Command Line

1. Open a terminal or command prompt.
2. Navigate to the directory containing your database file.
3. Run the following command to open the SQLite command-line tool:
   ```sh
   sqlite3 weather.db
   ```
4. Once inside the SQLite prompt, you can run SQL queries to view the data. For example:
   ```sql
   .tables  -- List all tables
   SELECT * FROM weather;  -- View data in the weather table
   SELECT * FROM predefined_cities;  -- View data in the predefined_cities table
   ```

## Development

To run the application in development mode:

1. Start the backend:

   ```sh
   uvicorn app.main:app --reload
   ```

2. Start the frontend:

   ```sh
   cd weather-dashboard-ui
   npm install
   npm start
   ```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## License

This project is licensed under the MIT License.