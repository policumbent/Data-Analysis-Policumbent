import pandas as pd


def controllo(fl):
    df = pd.read_csv(fl)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    

def main():
    file = '../../dati/BM_23/Cerberus/Diego_16_09_2023_AM_2.csv'
    controllo(file)


main()