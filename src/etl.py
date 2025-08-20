import pandas as pd
import sqlite3


def load_flight_data():
    """ Load flight data """
    return pd.read_csv("data/raw/flights.csv")


def load_weather_data():
    """ Load weather data """
    return pd.read_csv("data/raw/weather.csv")


def configure():
    pd.options.display.max_columns = None


def transform_flights(flights: pd.DataFrame) -> pd.DataFrame:
    flights["date_fl"] = (
            pd.to_datetime(dict(year=flights["year"], month=flights["month"], day=1))
            .dt.strftime("%Y-%m-%d")
    )
    return flights


#Load into SQLite
def load_flights(transformed_flights: pd.DataFrame, sqlite_path: str) -> None:

    with sqlite3.connect(sqlite_path) as conn:
        flights.to_sql('jfk_flights',conn,if_exists='replace',index=False)


if __name__ == "__main__":
    configure()

    # extract
    raw_flights = load_flight_data()
    # print(flights.head())

    raw_weather = load_weather_data()
    # print(weather.head())

    # transform
    flights = transform_flights(raw_flights)
    print(flights[["year", "month", "date_fl"]].head())

    # load
    load_flights(flights, "data/processed/jfk_data.db")
    print("First data pipeline complete")

