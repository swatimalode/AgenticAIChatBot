from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
WEATHER_API = os.getenv("WEATHER_API")
GEOCODER_API = os.getenv("GEOCODER_API")