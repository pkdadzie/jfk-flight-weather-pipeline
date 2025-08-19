import pandas as pd
import sqlite3


#extract data;

# Load flight data
flights= pd.read_csv("data/raw/flights.csv")
weather=pd.read_csv("data/raw/weather.csv")

# Check the first few rows
pd.options.display.max_columns = None
print(flights.head())
print(weather.head())

# Check column types
weather.dtypes
flights.shape

#Transform
#flights['FL_DATE']=pd.to_datetime(flights['FL_DATE'])

flights["date_fl"] = pd.to_datetime(dict(year=flights["year"], month=flights["month"], day=1))

flights["date_fl"] = flights["date_fl"].dt.strftime("%Y-%m-%d")

flights['FL_DATE']=pd.to_datetime(flights['date_fl'])

# View the result
print(flights[["year", "month", "date_fl"]].head())



#Load into SQLite
conn=sqlite3.connect('data/processed/jfk_data.db')
flights.to_sql('jfk_flights',conn,if_exists='replace',index=False)
conn.close()

print("First data pipeline complete")







