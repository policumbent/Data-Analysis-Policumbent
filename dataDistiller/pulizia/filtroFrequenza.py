import pandas as pd
import matplotlib.pyplot as plt


def hearthrate(inpF, outF):
    df = pd.read_csv(inpF)

    # Converte la colonna timestamp in datetime e tronca ai secondi
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['second'] = df['timestamp'].dt.floor('S')

    # Calcola la media per ogni secondo
    df_avg = df.groupby('second')['heartrate'].mean().reset_index()
    df_avg.rename(columns={'second': 'timestamp', 'heartrate': 'avg_heartrate'}, inplace=True)


    df_avg.to_csv(outF, index=False)
    print(f"Salvato: {outF}")


def powermeter(inpF, outF):
    df = pd.read_csv(inpF)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # rimuove righe con timestamp non validi

    df['second'] = df['timestamp'].dt.floor('S')

    df_avg = df.groupby('second')[['power', 'instant_power', 'cadence']].mean().reset_index()
    df_avg.rename(columns={'second': 'timestamp'}, inplace=True)


    df_avg.to_csv(outF, index=False)
    print(f"Salvato: {outF}")


def unifica(inpF, inpF2, outF):
    df1 = pd.read_csv(inpF)
    df2 = pd.read_csv(inpF2)

    df1['timestamp'] = pd.to_datetime(df1['timestamp'], errors='coerce')
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], errors='coerce')


    #seleziono colonne da unire

    df1_sel = df1[['timestamp', 'power', 'instant_power', 'cadence']]
    df2_sel = df2[['timestamp', 'avg_heartrate']]

    df_merged = pd.merge(df1_sel, df2_sel, on='timestamp', how='inner')

    df_merged.to_csv(outF, index=False)


def controlloRigheNulle(inpF, outF):
    df = pd.read_csv(inpF)
    
    #ricerco righe con valori nulli
    r0 = (df[['power', 'instant_power', 'cadence', 'avg_heartrate']] == 0).sum()
    #print(r0)

    righe_nulle = (df['cadence'] == 0) | (df['instant_power'] == 0)

    df_zeri = df[righe_nulle].copy()
    print(df_zeri)

    df_zeri['timestamp'] = pd.to_datetime(df_zeri['timestamp'])
    intervalli = df_zeri['timestamp'].diff().dropna()

    intervalli_filtrati = intervalli[intervalli < pd.Timedelta(seconds=600)]

    print(intervalli.describe())
    print(intervalli_filtrati.describe())

    plt.figure(figsize=(10, 4))
    plt.plot(intervalli_filtrati.dt.total_seconds().values, marker='o')
    plt.title("Intervalli tra righe con cadence=0 o instant_power=0")
    plt.xlabel("Indice evento")
    plt.ylabel("Intervallo (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
   


def main():
    inpF = '../../dati/cerberus/balocco/20250614/run2/run2.csv'
    inpF2 = '../../dati/cerberus/balocco/20250614/run2/hearthrateR1.csv'
    outF = '../../dati/cerberus/balocco/20250614/run2/run2.csv'

    inp = input('(1) hearthrate, (2) powermeter, (3) unifica, (4) controlla: ')

    if inp == '1':
        hearthrate(inpF, outF)
    
    elif inp == '2':
        powermeter(inpF, outF)
    
    elif inp == '3':
        unifica(inpF, inpF2, outF)
    
    elif inp == '4':
        controlloRigheNulle(inpF, outF)
    

main()

