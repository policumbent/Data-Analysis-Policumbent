import pandas as pd


def hearthrate():
    inpF = '../../dati/cerberus/balocco/20250614/rowdata/run2/hearthrate_13-06-2025@18_01_30.csv'
    outF = '../../dati/cerberus/balocco/20250614/run2/hearthrateR1.csv'


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


def powermeter():
    inpF = '../../dati/cerberus/balocco/20250614/rowdata/run2/powermeter_13-06-2025@18_01_30.csv'
    outF = '../../dati/cerberus/balocco/20250614/run2/pwmR1'


    df = pd.read_csv(inpF)

    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # rimuove righe con timestamp non validi

    df['second'] = df['timestamp'].dt.floor('S')

    df_avg = df.groupby('second')[['power', 'instant_power', 'cadence']].mean().reset_index()
    df_avg.rename(columns={'second': 'timestamp'}, inplace=True)


    df_avg.to_csv(outF, index=False)
    print(f"Salvato: {outF}")


def main():
    inp = input('(1) hearthrate, (2) powermeter: ')
    if inp == '1':
        hearthrate()
    
    elif inp == '2':
        powermeter()
    
    
main()

