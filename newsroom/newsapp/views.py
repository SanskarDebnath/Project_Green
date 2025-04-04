import requests
import geocoder
from datetime import datetime
from django.shortcuts import render

def get_location():
    """Detects the user's latitude and longitude based on their IP."""
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng[0], g.latlng[1], g.city, g.country
    else:
        return 51.5074, -0.1278, "London", "GB" 


def get_aqi(latitude, longitude, api_key):
    """Fetches Air Quality Index (AQI) and categorizes it as Good, Bad, or Very Bad."""
    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(aqi_url)

    if response.status_code == 200:
        aqi_data = response.json()
        aqi_value = aqi_data["list"][0]["main"]["aqi"]

        # Categorizing AQI
        aqi_description = "Good" if aqi_value in [1, 2] else "Bad" if aqi_value in [3, 4] else "Very Bad"

        return aqi_value, aqi_description
    return None, "AQI Data Unavailable"




def index(request):
    latitude, longitude, city, country = get_location()  # Get user's location

    api_key = "fe20c54948a6a5d97117500bdaa09bd8"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    response = requests.get(url)
    aqi_value, aqi_description = get_aqi(latitude, longitude, api_key)  # Get AQI
    
    if response.status_code == 200:
        weather_data = response.json()

        formatted_data = {
            "city": city,
            "country": country,
            "temperature": weather_data["main"].get("temp", "N/A"),
            "feels_like": weather_data["main"].get("feels_like", "N/A"),
            "humidity": weather_data["main"].get("humidity", "N/A"),
            "pressure": weather_data["main"].get("pressure", "N/A"),
            "condition": weather_data["weather"][0].get("description", "N/A").capitalize(),
            "icon": weather_data["weather"][0].get("icon", ""),
            "wind_speed": weather_data["wind"].get("speed", "N/A"),
            "timestamp": datetime.utcfromtimestamp(weather_data["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
            "visibility": weather_data.get("visibility", "N/A"),
            "rain": weather_data.get("rain", {}).get("1h", "0"),  # Rainfall in last 1 hour
            "aqi": aqi_value,
            "aqi_description": aqi_description,  # Updated AQI description
            "sunrise": datetime.utcfromtimestamp(weather_data["sys"]["sunrise"]).strftime('%H:%M:%S'),
            "sunset": datetime.utcfromtimestamp(weather_data["sys"]["sunset"]).strftime('%H:%M:%S'),
        }
    else:
        formatted_data = {"error": "Failed to fetch weather data"}

    return render(request, 'index.html', {"weather": formatted_data})


def privacy_policy(request):
    return render (request, 'privacypolicy.html')