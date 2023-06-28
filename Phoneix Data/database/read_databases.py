import sqlite3
import pandas as pd

con = sqlite3.connect('2023-06-27.db')

data = pd.read_sql_query('Select * from ant', con)

# print(data.head())
data.to_csv('2023-06-27.csv', index=False)


