from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Weather response model
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    icon_url: str
    lat: float
    lon: float

# Route to fetch weather
@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = "New York"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {
            "city": city,
            "temperature": 0.0,
            "description": "Unavailable",
            "humidity": 0,
            "wind_speed": 0.0,
            "icon_url": "",
            "lat": 0.0,
            "lon": 0.0,
        }

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "icon_url": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }
