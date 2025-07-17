import pandas as pd
import matplotlib.pyplot as plt
from math import pi


file1 = '../../dati/cerberus/balocco/20250614/run1/run4.csv'        

df1 = pd.read_csv(file1)

df1['coppia'] = df1['power']/(df1['cadence']*(2*pi/60))

df1['timestamp'] = pd.to_datetime(df1['timestamp'], errors='coerce')

plt.figure(figsize=(12, 6))


for col in ['cadence']:
    plt.plot(df1['timestamp'], df1[col], label=f"cadenza : {col}")



plt.xlabel("Tempo")
plt.ylabel("Valori")
plt.title("Plot Dati da due File CSV")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#rifare il file run1.csv in run1