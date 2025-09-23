import os  
import json  
import sqlite3  
from datetime import datetime  
from JFK_flight_api import FlightAPI  
from jfk_weather import JFKWeatherAPI  
  
API_KEY_FLIGHT = os.getenv("b22993771b8db526adc3039545c57840"  , "b22993771b8db526adc3039545c57840")  
API_KEY_WEATHER = os.getenv("49646dfd48c24244963230606251609"  , "49646dfd48c24244963230606251609")  
DB_PATH = "data/jfk_flights_weather_history.sqlite3"  
  
DEVELOPMENT_MODE = False  
SAMPLE_FLIGHTS_FILE = "sample_flights.json"  
SAMPLE_WEATHER_FILE = "sample_weather.json"  
  
def save_sample_data(filename, data):  
    with open(filename, 'w') as f:  
        json.dump(data, f, indent=2)  
  
def load_sample_data(filename):  
    with open(filename, 'r') as f:  
        return json.load(f)  
  
def create_table(cursor):  
    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS flights_with_weather (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            flight_number TEXT,  
            airline TEXT,  
            departure_airport TEXT,  
            arrival_airport TEXT,  
            departure_time TEXT,  
            arrival_time TEXT,  
            status TEXT,  
            temperature_c REAL,  
            condition TEXT,  
            humidity INTEGER,  
            wind_kph REAL,  
            weather_timestamp TEXT  
        )  
    """)  
  
def load_data():  
    """  
    Fetch and store **current** flight + weather data for JFK.  
    """  
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  
  
    conn = sqlite3.connect(DB_PATH)  
    cursor = conn.cursor()  
    create_table(cursor)  
  
    flight_api = FlightAPI(API_KEY_FLIGHT)  
    weather_api = JFKWeatherAPI(API_KEY_WEATHER)  
  
    if DEVELOPMENT_MODE:  
        print("Development Mode: Loading data from saved JSON...")  
        flights_raw = load_sample_data(SAMPLE_FLIGHTS_FILE)  
        weather_raw = load_sample_data(SAMPLE_WEATHER_FILE)  
    else:  
        print("Live Mode: Fetching current data...")  
        flights_raw = flight_api.get_flights_by_airport(airport_code="JFK")  
        save_sample_data(SAMPLE_FLIGHTS_FILE, flights_raw)  
  
        weather_raw = weather_api.get_current_weather()  
        save_sample_data(SAMPLE_WEATHER_FILE, weather_raw)  
  
    parsed_flights = flight_api.parse_flight_data(flights_raw)  
  
    try:  
        # Current weather only  
        temp_c = weather_raw["current"]["temp_c"]  
        condition = weather_raw["current"]["condition"]["text"]  
        humidity = weather_raw["current"]["humidity"]  
        wind_kph = weather_raw["current"]["wind_kph"]  
        weather_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    except (TypeError, KeyError) as e:  
        print(f"Weather data missing or invalid: {e}")  
        return  
  
    for f in parsed_flights:  
        cursor.execute("""
    INSERT INTO flights_with_weather (
        flight_number, airline, departure_airport, arrival_airport,
        departure_time, arrival_time, status,
        temperature_c, condition, humidity, wind_kph, weather_timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    f['flight_number'], f['airline'], f['departure_airport'], f['arrival_airport'],
    f['departure_time'], f['arrival_time'], f['status'],
    temp_c, condition, humidity, wind_kph, weather_timestamp
))
 
  
    conn.commit()  
    conn.close()  
    print(f"Added {len(parsed_flights)} flights with weather snapshot for current date")  
  
  
if __name__ == "__main__":   
    load_data()  # Only current data now  