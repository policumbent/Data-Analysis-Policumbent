import sqlite3
import pandas as pd

con = sqlite3.connect('database.db')

data = pd.read_sql_query('Select * from ant', con)

# print(data.head())
data.to_csv('ant.csv', index=False)


