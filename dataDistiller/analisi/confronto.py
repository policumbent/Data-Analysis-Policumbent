import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit


def modello_quadratico(v, a, b, c):
    return a*v**2 + b*v + c


path = '../../dati/Phoenix/Enzo'

lDiz = list()

for nf in os.listdir(path):
    pathC = os.path.join(path, nf)
    df = pd.read_csv(pathC)
    mnPower = df['power'].mean()
    maxPower = df['power'].max()

    mnSpeed = df['speed'].mean()
    maxSpeed = df['speed'].max()

    diz = {
        'run' : nf,
        'mean Power' : mnPower,
        'max Power' : maxPower,
        'mean speed' : mnSpeed,
        'max speed' : maxSpeed
    }

    lDiz.append(diz)

    pr = False

    if pr:
        print(nf)
        print(f'Potenza media: {mnPower} W, potenza massima: {maxPower} W')
        print(f'Velocità media: {mnSpeed} km/h, velocità massima: {maxSpeed} km/h')


df = pd.DataFrame(lDiz)
df = df.sort_values(by = 'mean Power').reset_index(drop=True)

print(df)

speedTarget = 150
degree = 2


linear = False
if linear:
    x = df['max speed'].values.reshape(-1,1)
    y_mean = df['mean Power'].values
    y_max = df['max Power'].values

    regMean = LinearRegression().fit(x, y_mean)
    regMax = LinearRegression().fit(x, y_max)

    newPowerMean = regMean.predict([[speedTarget]])[0]
    newPowerMax = regMax.predict([[speedTarget]])[0]

    print(f'Linear regression: potenza media = {round(newPowerMean,2)} W potenza massima = {round(newPowerMax,2)} W')


parabolic = True
if parabolic:
    fit_mean, _ = curve_fit(modello_quadratico, df['max speed'], df['mean Power'])
    fit_max, _ = curve_fit(modello_quadratico, df['max speed'], df['max Power'])

    newPowerMean = modello_quadratico(speedTarget, *fit_mean)
    newPowerMax = modello_quadratico(speedTarget, *fit_max)

    print(f'Polynomial regression: potenza media = {round(newPowerMean,2)} W potenza massima = {round(newPowerMax,2)} W')


plot = True
if plot:
    vel_range = np.linspace(80, 200, 100)
    plt.scatter(df['max speed'], df['mean Power'])
    plt.plot(vel_range, modello_quadratico(vel_range, *fit_mean), "--r")

    # Punto stimato
    plt.scatter([speedTarget], [newPowerMean], color="blue", marker="x", s=100)
    plt.title("Regressione non lineare di secondo grado")

    #plt.plot(df['mean Power'], df['max speed'])
    plt.ylabel('mean Power [W]')
    plt.xlabel('max Speed [Km/h]')
    plt.show()