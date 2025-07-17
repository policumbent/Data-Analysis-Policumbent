import pandas as pd


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


def main():
    inpF = '../../dati/cerberus/balocco/20250614/run1/pwmR1.csv'
    inpF2 = '../../dati/cerberus/balocco/20250614/run1/hearthrateR1.csv'
    outF = '../../dati/cerberus/balocco/20250614/run1/run1.csv'

    inp = input('(1) hearthrate, (2) powermeter, (3) unifica: ')

    if inp == '1':
        hearthrate(inpF, outF)
    
    elif inp == '2':
        powermeter(inpF, outF)
    
    elif inp == '3':
        unifica(inpF, inpF2, outF)
    

main()

