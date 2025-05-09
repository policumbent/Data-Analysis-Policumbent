"""
Data: 15/12/2022
@author: felixackermann
@co-authors: alessandrogiraudo, andreapalizzi, gabrielevittori
"""
'''
Cosa fa questo codice?
È presto detto:
la stazione meteo del team POLICUMBENT annota in un file csv i dati relativi alle condizioni atmosferiche
(temperatura, pressione, umidità, velocità e direzione del vento). Da questo file, tramite opportuni calcoli
e considerazioni, si estrapolano informazioni sulle raffiche di vento e la loro distribuzione, in vista di un
possibile futuro contributo nell'ottimizzazione della struttura carenata della bicicletta
'''

#serve a Gab
#import os
#print(os.chdir("C:\\Users\\utente\\Desktop\\UNI\\TEAM_POLICUMBENT\\nuovo_codice_python"))

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
import util
from intervallo import Intervallo

param_1 = 1.3
param_2 = 0.85
param_3 = 5
param_4 = 3
param_5 = 4
param_6 = 15

def main(file, grafici_da_disegnare=None):
    f_in = file
    M = util.leggi_file(f_in)
    t = M[:,0]
    n_rows = M.shape[0]

    T = M[:,1] # temperatura
    u = M[:,2] # umidità
    p = M[:,3] # pressione
    v = M[:,4] # velocità
    d = M[:,5] # direzione vento

    T, n_rid = util.media_mobile(T, param_4)
    u, n_rid = util.media_mobile(u, param_4)
    p, n_rid = util.media_mobile(p, param_4)
    v, n_rid = util.media_mobile(v, param_4)
    d, n_rid = util.media_mobile(d, param_4)


    # Creazione intervalli
    intervalli = [] 
    ts = util.primo_ts(M[0][0], param_6)
    while ts < M[len(M)-1][0]:
        ts_fine = ts + timedelta(minutes = param_6)
        intervalli.append(Intervallo(ts, ts_fine))
        ts = ts_fine

    # Inserimento dati negli intervalli
    j = 0
    for i in range(n_rows):
        while j < len(intervalli) and not intervalli[j].ammette(M[i][0]):
            j += 1
        intervalli[j].inserisci(M[i])

    if "1" in grafici_da_disegnare:
        util.trova_raffiche(M, intervalli, param_1, param_2, param_3, disegna=True)
    else:
        util.trova_raffiche(M, intervalli, param_1, param_2, param_3, disegna=False)
    
    if "2" in grafici_da_disegnare:
        util.temp_num_raff(intervalli)

    if "3" in grafici_da_disegnare:
        util.direzione_tempo_intensita(t, d, v, intervalli)
    
    if "4" in grafici_da_disegnare:
        plt.plot_date(t[1:-1],T, markersize=1)
        plt.plot_date(t[1:-1],(p-min(p))*10, markersize=1)
        plt.plot_date(t[1:-1],u, markersize=1)
        plt.plot_date(t[1:-1],v*10, markersize=1)
        plt.legend(["Temperatura", "Pressione", "Umidità", "Intensità"])
        plt.show()

    if "5" in grafici_da_disegnare:
        plt.plot(T, markersize=1)
        plt.plot((p-min(p))*10, markersize=1)
        plt.plot(u, markersize=1)
        plt.plot(v*10, markersize=1)
        plt.legend(["Temperatura", "Pressione", "Umidità", "Intensità"])
        plt.show()

for file in ["..\\Dataset\\2022_9_13_new.csv", "..\\Dataset\\2022_9_14_new.csv", "..\\Dataset\\2022_9_15_new.csv", "..\\Dataset\\2022_9_16_new.csv"]:
    main(file, "5")
