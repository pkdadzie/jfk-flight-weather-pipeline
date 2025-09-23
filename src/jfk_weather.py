"""  
weather_jfk.py  
Provides a class to interact with WeatherAPI for current, forecast,  
and historical weather data at JFK Airport.  
"""  
  
import logging  
from typing import Optional, Dict  
import requests  
  
# Configure logging  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
  
class JFKWeatherAPI:  
    BASE_URL = "http://api.weatherapi.com/v1"  
    JFK_LOCATION = "40.6413,-73.7781"  # Latitude,Longitude of JFK Airport  
  
    def __init__(self, api_key: str, timeout: int = 10) -> None:  
        if not api_key:  
            raise ValueError("API key must be provided.")  
        self.api_key = api_key  
        self.timeout = timeout  
  
    def _get_weather_data(self, endpoint: str, params: Dict) -> Optional[Dict]:  
        """Internal helper to request weather data."""  
        try:  
            response = requests.get(endpoint, params=params, timeout=self.timeout)  
            response.raise_for_status()  
            data = response.json()  
            logger.info(f"Weather API call successful (status {response.status_code})")  
            return data  
        except requests.exceptions.RequestException as e:  
            logger.error(f"Weather API request failed: {e}")  
            return None  
  
    def get_current_weather(self) -> Optional[Dict]:  
        endpoint = f"{self.BASE_URL}/current.json"  
        params = {"key": self.api_key, "q": self.JFK_LOCATION}  
        return self._get_weather_data(endpoint, params)  
  
    def get_forecast(self, days: int = 3) -> Optional[Dict]:  
        endpoint = f"{self.BASE_URL}/forecast.json"  
        params = {"key": self.api_key, "q": self.JFK_LOCATION, "days": days}  
        return self._get_weather_data(endpoint, params)  
  
    def get_historical_weather(self, date: str) -> Optional[Dict]:  
        endpoint = f"{self.BASE_URL}/history.json"  
        params = {"key": self.api_key, "q": self.JFK_LOCATION, "dt": date}  
        return self._get_weather_data(endpoint, params)  
  
    def parse_current_weather(self, data: Dict) -> Optional[Dict]:  
        if not data:  
            return None  
        current = data.get("current", {})  
        location = data.get("location", {})  
        return {  
            "location": location.get("name"),  
            "temperature_c": current.get("temp_c"),  
            "condition": current.get("condition", {}).get("text"),  
            "wind_kph": current.get("wind_kph"),  
            "humidity": current.get("humidity")  
        }  
  
    def parse_historical_weather(self, data: Dict) -> Optional[Dict]:  
        """  
        Extract historical weather data from API response.  
        """  
        if not data:  
            return None  
        try:  
            forecast_day = data["forecast"]["forecastday"][0]["day"]  
            location = data.get("location", {})  
            return {  
                "location": location.get("name"),  
                "temperature_c": forecast_day.get("avgtemp_c"),  
                "condition": forecast_day.get("condition", {}).get("text"),  
                "wind_kph": forecast_day.get("maxwind_kph"),  
                "humidity": forecast_day.get("avghumidity"),  
                "date": data["forecast"]["forecastday"][0]["date"]  
            }  
        except (KeyError, IndexError) as e:  
            logger.error(f"Error parsing historical weather data: {e}")  
            return None  