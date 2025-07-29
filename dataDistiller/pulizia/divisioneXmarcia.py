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
    plot = False

    if plot:
        pl.figure(1)
        pl.plot(df['timestamp'], df['cadence'])
        pl.plot(df['timestamp'], df['speed'])


    d = 0.93
    p = list()

    for i in range(len(df)):
        if i >= 1:
            if df['cadence'][i] < (df['cadence'][i-1]) * d:
                p.append(i)

                if plot:
                    pl.axvline(df['timestamp'][i])
                
   
    if plot:
        pl.show()

    return p


def interpola(df, p):
    degree = 2
    poly = PolynomialFeatures(degree=degree)
    x_range = np.linspace(40, 100, 100).reshape(-1, 1)
    a = 0
    b = 1

    for i in p:
        X = df['cadence'][a:i].values.reshape(-1, 1)
        y = df['coppia'][a:i].values

        X_poly = poly.fit_transform(X)
        model = LinearRegression().fit(X_poly, y)

        x_range_poly = poly.transform(x_range)
        y_pred = model.predict(x_range_poly)

        pl.plot(x_range, y_pred, label = f'marcia {b}')
        b+=1

        
        a = i
    
    X = df['cadence'].values.reshape(-1, 1)
    y = df['coppia'].values

    X_poly = poly.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)

    x_range_poly = poly.transform(x_range)
    y_pred = model.predict(x_range_poly)

    pl.plot(x_range, y_pred, label = 'tot')


    pl.legend()
    pl.show()


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
    

def main():
    file = '../../dati/cerberus/nevada/20230916/Diego_16_09_2023_AM_2.csv'
    df = pd.read_csv(file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['coppia'] = df['instant_power']/(df['cadence']*(pi/30))

    controllo = False
    divisione = False
    interpola = False
    analisi = False

    if controllo:
        p = controllo(df)

    if interpola:
        interpola(df, p)

    if analisi:  
        analisi(df, p)

    if divisione:
        creaFile(df, p)



main()