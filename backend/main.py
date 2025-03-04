from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from typing import List, Optional
import joblib
import numpy as np
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = FastAPI(title="Weather Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    description: str
    prediction_high: Optional[float]
    prediction_low: Optional[float]
    rain_probability: Optional[float]

@app.get("/")
async def read_root():
    return {"message": "Weather Prediction API"}

@app.get("/weather/{city}", response_model=WeatherData)
async def get_weather(city: str):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Get current weather data
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 401:
            raise HTTPException(status_code=500, detail="Invalid API key. Please check your OpenWeatherMap API key")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")
        elif response.status_code != 200:
            error_data = response.json()
            raise HTTPException(status_code=500, detail=f"OpenWeatherMap API Error: {error_data.get('message', 'Unknown error')}")
            
        response.raise_for_status()
        data = response.json()

        # Extract relevant weather data
        current_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        # TODO: Load ML models and make predictions
        # For now, return dummy predictions
        prediction_high = current_temp + 5
        prediction_low = current_temp - 5
        rain_probability = 0.3 if "rain" in description.lower() else 0.1

        return WeatherData(
            temperature=current_temp,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            description=description,
            prediction_high=prediction_high,
            prediction_low=prediction_low,
            rain_probability=rain_probability
        )

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error accessing OpenWeatherMap API: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 