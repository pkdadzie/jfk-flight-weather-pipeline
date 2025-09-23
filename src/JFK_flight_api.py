"""  
flight_api.py  
Provides a class to interact with the AviationStack API for flight data.  
Includes methods for current and historical flights and parsing flight details.  
"""  
  
import logging  
from typing import List, Dict  
import requests  
  
# Configure logging  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
  
class FlightAPI:  
    def __init__(self, api_key: str) -> None:  
        """  
        Initialize the FlightAPI instance.  
        :param api_key: Your AviationStack API key.  
        """  
        if not api_key:  
            raise ValueError("API key must be provided.")  
        self.api_key = api_key  
        self.base_url = "https://api.aviationstack.com/v1/flights"  
  
    def get_flights_by_airport(self, airport_code: str = "JFK", limit: int = 100) -> List[Dict]:  
        """  
        Retrieve current flights departing from a given airport.  
        :param airport_code: IATA code of the departure airport.  
        :param limit: Maximum number of results.  
        :return: List of flight data dictionaries.  
        """  
        params = {  
            "access_key": self.api_key,  
            "dep_iata": airport_code,  
            "limit": limit  
        }  
        try:  
            response = requests.get(self.base_url, params=params, timeout=10)  
            response.raise_for_status()  
            data = response.json()  
            flights = data.get("data", [])  
            logger.info(f"Retrieved {len(flights)} flights from {airport_code}")  
            return flights  
        except requests.RequestException as e:  
            logger.error(f"API request failed: {e}")  
            return []  
  
    def get_historical_flights(self, airport_code: str = "JFK", date: str = "2025-09-21", limit: int = 100) -> List[Dict]:  
        """  
        Retrieve historical flights for a given airport and date.  
        :param airport_code: IATA code of the departure airport.  
        :param date: Date in YYYY-MM-DD format.  
        :param limit: Maximum number of results.  
        :return: List of flight data dictionaries.  
        """  
        params = {  
            "access_key": self.api_key,  
            "dep_iata": airport_code,  
            "flight_date": date,  
            "limit": limit  
        }  
        try:  
            response = requests.get(self.base_url, params=params, timeout=10)  
            response.raise_for_status()  
            data = response.json()  
            flights = data.get("data", [])  
            logger.info(f"Retrieved {len(flights)} historical flights from {airport_code} on {date}")  
            return flights  
        except requests.RequestException as e:  
            logger.error(f"Historical API request failed: {e}")  
            return []  
  
    def parse_flight_data(self, flights: List[Dict]) -> List[Dict]:  
        """  
        Parse raw flight data into a simplified structure.  
        :param flights: List of raw flight dictionaries from the API.  
        :return: List of parsed flight dictionaries.  
        """  
        parsed = []  
        for flight in flights:  
            parsed.append({  
                "flight_number": flight.get("flight", {}).get("iata"),  
                "airline": flight.get("airline", {}).get("name"),  
                "departure_airport": flight.get("departure", {}).get("airport"),  
                "arrival_airport": flight.get("arrival", {}).get("airport"),  
                "departure_time": flight.get("departure", {}).get("scheduled"),  
                "arrival_time": flight.get("arrival", {}).get("scheduled"),  
                "status": flight.get("flight_status")  
            })  
        return parsed  