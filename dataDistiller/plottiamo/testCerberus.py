import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
      

def plot(file1):
    inp = input('(1) plot, (2) plot più punti nulli interpolati: ')

    df1 = pd.read_csv(file1)

    df1['coppia'] = df1['instant_power']/(df1['cadence']*(2*pi/60))
    print(df1[df1['coppia'] == np.inf])

    df1['timestamp'] = pd.to_datetime(df1['timestamp'], errors='coerce')

    plt.figure(figsize=(12, 6))


    for col in ['coppia', 'cadence', 'instant_power', 'avg_heartrate']:
        plt.plot(df1['timestamp'], df1[col], label=f"{col}")
    
    if inp == '2':
        file = '../../dati/cerberus/balocco/20250614/run2/run2.csv'
        df = pd.read_csv(file)
        mask_zero = (df['cadence'] == 0) | (df['instant_power'] == 0)
        ts_zero = pd.to_datetime(df.loc[mask_zero, 'timestamp'])


        for ts in ts_zero:
            plt.axvline(x=ts, color='red', linestyle='--', alpha=0.5)
        

    plt.xlabel("Tempo")
    plt.ylabel("Valori")
    plt.title("Run 2 con interpolazione")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def medDev(file):
    df = pd.read_csv(file)

    i = False

    if i:
        start = pd.to_datetime("2025-06-13 16:40:00")
        end   = pd.to_datetime("2025-06-13 16:50:00")

        df_interval = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]

        df_interval[['instant_power', 'cadence', 'power', 'avg_heartrate']].agg(['mean', 'std']).T

        print(df['df_interval'])

    else:
        df['coppia'] = df['instant_power']/(df['cadence']*(2*pi/60))

        media1 = df['instant_power'].mean()
        media2 = df['coppia'].mean()

        dev1 = df['instant_power'].std(ddof=0)
        dev2 = df['coppia'].std(ddof=0)

        print(f'cadenza: media: {media1:.2f}, deviazione standard {dev1:.2f}')
        print(f'freC: media: {media2:.2f}, deviazione standard {dev2:.2f}')
    

def coppiaCadenza():
    file_label = [
        #('../../dati/cerberus/balocco/20250614/run1/run1.csv', 'Run 1.1'),
        #('../../dati/cerberus/balocco/20250614/run1/run2.csv', 'step 1'),
        #('../../dati/cerberus/balocco/20250614/run1/run3_interpolato.csv', 'step 2'),
        #('../../dati/cerberus/balocco/20250614/run1/run4.csv', 'step 3'),
        ('../../dati/cerberus/balocco/20250614/run2/run2_interpolato.csv', 'Run 2')
    ]

    # Setup fit
    degree = 2
    poly = PolynomialFeatures(degree=degree)
    x_range = np.linspace(40, 100, 200).reshape(-1, 1)  # range comune

    #plt.figure(figsize=(10, 6))

    for file, label in file_label:
        df = pd.read_csv(file)
        df['coppia'] = df['instant_power']/(df['cadence']*(2*pi/60))
        X = df['cadence'].values.reshape(-1, 1)
        y = df['coppia'].values

        X_poly = poly.fit_transform(X)
        model = LinearRegression().fit(X_poly, y)

        x_range_poly = poly.transform(x_range)
        y_pred = model.predict(x_range_poly)

        plt.plot(x_range, y_pred, label=f'{label} (fit)')
        plt.scatter(X, y, alpha=0.2, label=f'{label} dati')

    plt.xlabel('Cadenza (rpm)')
    plt.ylabel('Coppia (Nm)')
    plt.title('confronto fit - Coppia Cadenza')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def main():
    file = '../../dati/cerberus/balocco/20250614/run2/run2_interpolato.csv'  
    inp = input('(1) plot (2) media e deviazione, (3) interpolazione: ')

    if inp == '1':
        plot(file)

    elif inp == '2':
        medDev(file)
    
    elif inp == '3':
        coppiaCadenza()


main()