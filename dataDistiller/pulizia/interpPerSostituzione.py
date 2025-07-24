import pandas as pd


def manual_interpolation_all(df, colonna_timestamp='timestamp'):
    df = df.copy()
    df[colonna_timestamp] = pd.to_datetime(df[colonna_timestamp])
    df.reset_index(drop=True, inplace=True)

    # Colonne da interpolare (tutte tranne il timestamp)
    colonne_interpolabili = [c for c in df.columns if c != colonna_timestamp]

    # Trova righe "nulle"
    condizione = (df['cadence'] == 0) | (df['instant_power'] == 0)
    indici_nulli = df[condizione].index
    print(f"Trovati {len(indici_nulli)} punti nulli.")

    # Salviamo tutti gli indici da annullare
    indici_da_interpolare = set()

    for idx in indici_nulli:
        print(f"\n📍 Rilevato punto nullo all’indice {idx}")
        print(df.loc[max(0, idx-3):min(idx+3, len(df)-1), colonne_interpolabili])

        try:
            prima = int(input("Quante righe PRIMA vuoi includere nell’interpolazione? "))
            dopo = int(input("Quante righe DOPO? "))
        except ValueError:
            print("⚠️ Input non valido, salto il punto.")
            continue

        inizio = max(0, idx - prima)
        fine = min(len(df) - 1, idx + dopo)
        indici_da_interpolare.update(range(inizio, fine + 1))

    # Imposta a NaN tutte le colonne selezionate tranne timestamp
    for col in colonne_interpolabili:
        df.loc[list(indici_da_interpolare), col] = pd.NA
        df[col] = df[col].interpolate(method='linear')

    return df


def main():
    df = pd.read_csv('../../dati/cerberus/balocco/20250614/run2/run2.csv')

    df_modificato = manual_interpolation_all(df)

    df_modificato.to_csv('../../dati/cerberus/balocco/20250614/run2/run2_interpolato.csv', index=False)


main()
