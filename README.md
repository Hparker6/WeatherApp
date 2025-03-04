# Weather Prediction App

A modern weather application that provides real-time weather data and machine learning-based predictions for temperature and precipitation.

## Features

- Real-time weather data using OpenWeatherMap API
- Machine learning predictions for temperature highs/lows
- Precipitation probability forecasting
- Beautiful, responsive UI built with React and TailwindCSS
- FastAPI backend with ML model integration

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)

4. Create a `.env` file in the backend directory:
```bash
OPENWEATHERMAP_API_KEY=your_api_key_here
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Access the application at `http://localhost:3000`

## Project Structure

```
weather-app/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   ├── ml_models/
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── requirements.txt
``` 