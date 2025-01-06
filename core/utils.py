# core/utils.py
import requests
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_weather_data(city="Bwari"):
    """
    Fetch weather data from OpenWeatherMap API
    """
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        response = requests.get(
            base_url,
            params={
                'q': city,
                'appid': api_key,
                'units': 'metric'  # For Celsius
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'temperature': round(data['main']['temp']),
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'city': data['name'],
            'country': data['sys']['country'],
            'timestamp': datetime.now().strftime('%H:%M %p'),
            'icon_url': f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"
        }
        return weather_data
    
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return None