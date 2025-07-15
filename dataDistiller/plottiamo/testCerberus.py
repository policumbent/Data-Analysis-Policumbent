import pandas as pd
import matplotlib.pyplot as plt


file1 = '/Users/mario/Data-Analysis-Policumbent/dati/cerberus/balocco/20250614/run2/pwmR1.csv'   
file2 = '/Users/mario/Data-Analysis-Policumbent/dati/cerberus/balocco/20250614/run2/hearthrateR1.csv'      

colonne_da_plottare_file1 = ['instant_power'] 
colonne_da_plottare_file2 = ['avg_heartrate']


label_file1 = "Power"
label_file2 = "Heartrate"



df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

df1['coppia'] = df1['power']/(df1['cadence']*(2*3.14/60))

df1['timestamp'] = pd.to_datetime(df1['timestamp'], errors='coerce')
df2['timestamp'] = pd.to_datetime(df2['timestamp'], errors='coerce')



plt.figure(figsize=(12, 6))


for col in colonne_da_plottare_file1:
    plt.plot(df1['timestamp'], df1[col], label=f"{label_file1}: {col}")


for col in colonne_da_plottare_file2:
    plt.plot(df2['timestamp'], df2[col], label=f"{label_file2}: {col}")


for col in ['coppia']:
    plt.plot(df1['timestamp'], df1[col], label=f"coppia : {col}")


for col in ['cadence']:
    plt.plot(df1['timestamp'], df1[col], label=f'cadenza')

plt.xlabel("Tempo")
plt.ylabel("Valori")
plt.title("Plot Dati da due File CSV")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
