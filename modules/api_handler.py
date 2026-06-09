import os
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": round(data["main"]["temp"]),
                    "feels_like": round(data["main"]["feels_like"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "wind_speed": round(data["wind"]["speed"] * 3.6),
                    "min_temp": round(data["main"]["temp_min"]),
                    "max_temp": round(data["main"]["temp_max"]),
                }
            }
        elif response.status_code == 401:
            return {"success": False, "error": "Invalid weather API key."}
        elif response.status_code == 404:
            return {"success": False, "error": f"City '{city}' not found."}
        else:
            return {"success": False, "error": f"Error {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No internet connection."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_weather_emoji(description):
    description = description.lower()
    if "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description or "drizzle" in description:
        return "🌧️"
    elif "thunder" in description or "storm" in description:
        return "⛈️"
    elif "snow" in description:
        return "❄️"
    elif "mist" in description or "fog" in description or "haze" in description:
        return "🌫️"
    else:
        return "🌤️"


def get_coordinates(city):
    """
    Uses Nominatim (free, no API key) to get lat/lng for a city.
    """
    try:
        geolocator = Nominatim(user_agent="travel_assistant_app")
        location = geolocator.geocode(city, timeout=10)

        if location:
            return {
                "success": True,
                "lat": location.latitude,
                "lng": location.longitude,
                "address": location.address
            }
        else:
            return {"success": False, "error": f"Location '{city}' not found."}

    except Exception as e:
        return {"success": False, "error": f"Geocoding error: {str(e)}"}


def get_multiple_coordinates(cities):
    """
    Gets coordinates for a list of cities.
    Returns list of dicts with city name and coordinates.
    """
    results = []
    for city in cities:
        coords = get_coordinates(city)
        if coords["success"]:
            results.append({
                "city": city,
                "lat": coords["lat"],
                "lng": coords["lng"],
                "address": coords["address"]
            })
    return results