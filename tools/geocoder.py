import requests
from config import GEOCODER_API

def geocoder(address: str):
    headers = {
        "User-Agent": "swatimalode96@gmail.com"
    }

    response = requests.get(GEOCODER_API ,
        params={
            "q": address,
            "format": "json"
        },
        headers=headers
    )

    data = response.json()
    
    if data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return {"latitude": latitude, "longitude": longitude}
    else:
        return {"error": "Address not found."} 