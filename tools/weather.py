from config import WEATHER_API
import requests

def weather(latitude, longitude):
    url = f"{WEATHER_API}&latitude={latitude}&longitude={longitude}"
    result = requests.get(url)
    data = result.json()
    current = data["current"]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "temperature": current["temperature_2m"],
        "units": "Celsius",
        "time": current["time"]
    }
