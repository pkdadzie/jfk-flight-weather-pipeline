# flight_weather_insights.py
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_PATH = "data/jfk_flights_weather_history.sqlite3"

def main():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #0 Total Flights
    print("\n=== Total Flights ===")
    cursor.execute("SELECT COUNT(*) FROM flights_with_weather;")
    total_rows = cursor.fetchone()[0]
    print(f"Total rows in flights_with_weather: {total_rows}")

    # 1️ Daily Flight Count + Average Temperature
    print("\n=== Daily Flight Count + Average Temperature ===")
    query1 = """
        SELECT DATE(weather_timestamp) AS day,
               COUNT(*) AS total_flights,
               ROUND(AVG(temperature_c), 1) AS avg_temp_c
        FROM flights_with_weather
        GROUP BY day
        ORDER BY day;
    """
    cursor.execute(query1)
    for row in cursor.fetchall():
        print(f"{row[0]} → Flights: {row[1]}, Avg Temp: {row[2]}°C")



    # 2️ Most Common Flight Status
    print("\n=== Most Common Flight Status ===")
    query2 = """
        SELECT status, COUNT(*) AS count
        FROM flights_with_weather
        GROUP BY status
        ORDER BY count DESC;
    """
    cursor.execute(query2)
    for row in cursor.fetchall():
        print(f"{row[0]} → {row[1]} flights")

    # 3 Weather Conditions That Coincide With Delays
    print("\n=== Weather Conditions That Coincide With Delays ===")
    query3 = """
        SELECT condition, COUNT(*) AS delay_count
        FROM flights_with_weather
        WHERE status = 'delayed'
        GROUP BY condition
        ORDER BY delay_count DESC;
    """
    cursor.execute(query3)
    for row in cursor.fetchall():
        print(f"{row[0]} → {row[1]} delays")

    # 4️ Busiest Arrival Airports from JFK
    print("\n=== Busiest Arrival Airports from JFK ===")
    query4 = """
        SELECT arrival_airport, COUNT(*) AS flight_count
        FROM flights_with_weather
        GROUP BY arrival_airport
        ORDER BY flight_count DESC
        LIMIT 10;
    """
    cursor.execute(query4)
    for row in cursor.fetchall():
        print(f"{row[0]} → {row[1]} flights")

    # 5️ Hourly Flight Activity
    print("\n=== Hourly Flight Activity ===")
    query5 = """
        SELECT STRFTIME('%H', departure_time) AS hour_of_day,
               COUNT(*) AS flights
        FROM flights_with_weather
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
    """
    cursor.execute(query5)
    for row in cursor.fetchall():
        print(f"{row[0]}:00 → {row[1]} flights")

    # 6️ Average Delay by Weather Condition
    print("\n=== Average Delay by Weather Condition ===")
    query6 = """
        SELECT condition,
               ROUND(AVG(CASE WHEN status='delayed' THEN 1 ELSE 0 END)*100, 1) AS delay_rate_percent
        FROM flights_with_weather
        GROUP BY condition
        ORDER BY delay_rate_percent DESC;
    """
    cursor.execute(query6)
    for row in cursor.fetchall():
        print(f"{row[0]} → {row[1]}% delayed")

    # 7️ Average Temperature by Hour of Day
    print("\n=== Average Temperature by Hour of Day ===")
    query7 = """
        SELECT STRFTIME('%H', departure_time) AS hour_of_day,
               ROUND(AVG(temperature_c), 1) AS avg_temp_c
        FROM flights_with_weather
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
    """
    cursor.execute(query7)
    for row in cursor.fetchall():
        print(f"{row[0]}:00 → Avg Temp: {row[1]}°C")

    # 8️ Flights by Airline
    print("\n=== Flights by Airline ===")
    query8 = """
        SELECT airline, COUNT(*) AS flight_count
        FROM flights_with_weather
        GROUP BY airline
        ORDER BY flight_count DESC;
    """
    cursor.execute(query8)
    for row in cursor.fetchall():
        print(f"{row[0]} → {row[1]} flights")

    # 9️ Delays by Airline
    print("\n=== Delays by Airline ===")
    query9 = """
        SELECT airline,
               COUNT(*) AS total_flights,
               SUM(CASE WHEN status='delayed' THEN 1 ELSE 0 END) AS delayed_flights,
               ROUND(SUM(CASE WHEN status='delayed' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS delay_percent
        FROM flights_with_weather
        GROUP BY airline
        ORDER BY delay_percent DESC;
    """
    cursor.execute(query9)
    for row in cursor.fetchall():
        print(f"{row[0]} → Total: {row[1]}, Delayed: {row[2]}, Delay %: {row[3]}%")

    # Flights vs Wind Speed
    print("\n=== Flights vs Wind Speed ===")
    query10 = """
        SELECT 
            CASE 
                WHEN wind_kph < 10 THEN '0-10 kph'
                WHEN wind_kph < 20 THEN '10-20 kph'
                WHEN wind_kph < 30 THEN '20-30 kph'
                ELSE '30+ kph'
            END AS wind_range,
            COUNT(*) AS flights,
            SUM(CASE WHEN status='delayed' THEN 1 ELSE 0 END) AS delayed_flights
        FROM flights_with_weather
        GROUP BY wind_range
        ORDER BY wind_range;
    """
    cursor.execute(query10)
    for row in cursor.fetchall():
        print(f"{row[0]} → Flights: {row[1]}, Delayed: {row[2]}")

    # Close connection
    conn.close()
    print("\n All queries executed successfully.")

if __name__ == "__main__":
    main()
