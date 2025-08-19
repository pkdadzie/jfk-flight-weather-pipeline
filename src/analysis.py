import sqlite3
from matplotlib import pyplot as plt
import pandas as pd


conn=sqlite3.connect('data/processed/jfk_data.db')

#1. Find the number flights per day
q1=pd.read_sql("select date_fl,count(*) as total_flights from jfk_flights group by date_fl order by date_fl",conn)
print(q1.head())

import seaborn as sns

# Set Seaborn style
sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.lineplot(data=q1, x="date_fl", y="total_flights", marker='o')
plt.title("Number of Flights per Day")
plt.xlabel("Date")
plt.ylabel("Total Flights")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


