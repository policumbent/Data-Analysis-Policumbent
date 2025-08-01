import pandas as pd
import matplotlib.pyplot as pl
from math import pi
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


def creaFile(df, p):
    m = 1
    a = 0
    for i in p:
        dfM = df[a:i]
        dfM.to_csv(f'../../dati/cerberus/nevada/20230916/divMarcie/marcia{m}.csv', index=False)
        a = i
        m+=1


def controllo(df):
    plot = True

    if plot:
        pl.figure(1)
        for col in ['cadence', 'instant_power', 'coppia']:
            pl.plot(df['timestamp'], df[col], label=col)


    d = 0.93
    p = list()

    for i in range(len(df)):
        if i >= 1:
            if df['cadence'][i] < (df['cadence'][i-1]) * d:
                p.append(i)

                if plot:
                    pl.axvline(df['timestamp'][i])
                
   
    if plot:
        pl.legend()
        pl.show()

    return p


def interpola(df,val1, val2):
    plot = True
    degree = 2

    poly = PolynomialFeatures(degree=degree)
    
    x = df[val1].values.reshape(-1, 1)
    y = df[val2].values

    x_poly = poly.fit_transform(x)
    model = LinearRegression().fit(x_poly, y)

    y_pred = model.predict(x_poly)

    if plot:
        pl.figure('int')
        pl.scatter(df[val1], df[val2], label='punti')
        pl.plot(df[val1], y_pred, label='interpolazione')
        pl.xlabel('cadenza [rpm]')
        pl.ylabel('coppia [N/m]')
        pl.title('curva Coppia - Cadenza')
        pl.legend()
        pl.show()


    return y_pred
  

def analisi(df, p):
    pl.figure(1)
    for col in ['coppia', 'cadence', 'instant_power', 'speed']:
            pl.plot(df['timestamp'], df[col], label = col)
    pl.legend() 
    pl.show()
    a = 0
    for i in p:
        for col in ['coppia', 'cadence', 'instant_power', 'speed']:
            pl.plot(df['timestamp'][a:i], df[col][a:i], label = col)

        pl.legend()
        pl.show()

        pl.scatter(df['cadence'][a:i], df['coppia'][a:i])
        pl.show()
        a = i
    

def anMarcia(df):
    plot = True
    medDev = False
    newMean = True

    df['coppia'] = df['instant_power']/(df['cadence']*(pi/30))

    if newMean:
        df['power'] = np.ones((1, len(df))).T
        for i in range(len(df)):
            if i == 0:
                df['power'][i] = df['instant_power'][i]
            
            else:
                media = (df['instant_power'][i]+df['power'][i-1])/2
                df['power'][i] = media

        df['nCoppia'] = df['power']/(df['cadence']*(pi/30))

        
        interpola(df, 'cadence', 'coppia')

    if medDev:
        media = df['instant_power'].mean()
        dev = df['instant_power'].std(ddof=1)

        print(f'media: {media:.2f}, deviazione: {dev:.2f}')

    if plot:
        pl.figure('pot')
        for col in ['power', 'instant_power', 'cadence']:
            pl.plot(df['timestamp'], df[col], label = col)
        pl.legend()
        pl.show()


def main():
    control = True
    divisione = False
    analisiV = False
    analisiMarcia = False

    if control:
        file = '../../dati/rowData/csv_file/powermeter/powermeter_10-09-2024@07min2.csv'
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['coppia'] = df['instant_power']/(df['cadence']*(pi/30))

        p = controllo(df)

        if analisiV:  
            analisi(df, p)

        if divisione:
            creaFile(df, p)
    
    if analisiMarcia:
        file = '../../dati/cerberus/nevada/20230916/divMarcie/marcia5.csv'
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        anMarcia(df)


main()