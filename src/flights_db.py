import sqlite3
import os

def create_flight_table(db_path="db/jfk_data.sqlite3"): 
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor() 
  
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS flight_api_data ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            flight_number TEXT, 
            airline TEXT, 
            departure_airport TEXT, 
            arrival_airport TEXT, 
            departure_time TEXT, 
            arrival_time TEXT, 
            status TEXT 
        ); 
    """) 
  
    conn.commit() 
    conn.close()


def insert_flights(flights, db_path="db/jfk_data.sqlite3"): 
    """ 
    Inserts a list of flights into the database. 
    flights: List of dictionaries (parsed from FlightAPI.parse_flight_data) 
    """
    if not flights:
        print("No flights to insert.")
        return

    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor() 
  
    for flight in flights:
        try:
            cursor.execute(""" 
                INSERT INTO flight_api_data ( 
                    flight_number, 
                    airline, 
                    departure_airport, 
                    arrival_airport, 
                    departure_time, 
                    arrival_time, 
                    status 
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?) 
            """, ( 
                flight.get('flight_number'), 
                flight.get('airline'), 
                flight.get('departure_airport'), 
                flight.get('arrival_airport'), 
                flight.get('departure_time'), 
                flight.get('arrival_time'), 
                flight.get('status') 
            ))
        except Exception as e:
            print(f"Failed to insert flight: {flight}\nError: {e}")
  
    conn.commit() 
    conn.close()
