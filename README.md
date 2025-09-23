# ✈️🌤 JFK Flight & Weather Data ETL & Analytics Pipeline

## 📌 Overview
This project implements a **complete ETL + analytics workflow** that:

- Extracts real-time and historical flight data from the [AviationStack API](https://aviationstack.com/) and weather data from the [WeatherAPI](https://www.weatherapi.com/) for **John F. Kennedy International Airport (JFK)**.
- Transforms raw JSON into clean, structured records.
- Loads the combined dataset into a local SQLite database.
- Analyzes the stored data to produce operational and historical insights.

---

## 🛠 Tech Stack
- **Language**: Python 3.x
- **Libraries**: `requests`, `logging`, `sqlite3`, `json`, `matplotlib`
- **APIs**: AviationStack REST API, WeatherAPI REST API
- **Database**: SQLite

---

## 📂 Project Structure
```text
etl_pipeline/
│
├── flight_api.py               # AviationStack API interaction & parsing
├── weather_jfk.py               # WeatherAPI interaction & parsing
├── load_flight_weather.py       # ETL orchestration: fetch, parse, store
├── flight_weather_insights.py   # Analytical queries & reporting
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation



---

## 🧪 Example Output
=== Total Flights === 
Total rows in flights_with_weather: 150
=== Daily Flight Count + Average Temperature === 
2025-09-21 → Flights: 50, Avg Temp: 22.5°C 2025-09-22 → Flights: 60, Avg Temp: 21.8°C 
...


---

## 📈 Potential Extensions
- Historical ingestion for multiple dates.
- Airflow DAG for scheduled runs.
- Visualization dashboards (Plotly, Tableau, Power BI).
- Cloud deployment (AWS RDS, GCP Cloud SQL).
