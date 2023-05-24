#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:06:19 2022

@author: felixackermann
@co-authors: alessandrogiraudo, andreapalizzi, gabrielevittori
"""

#from IPython.display import clear_output
import csv
import os #
import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as plt_pyplot
#import pywt as pwt                          #pyWavelets
import statistics as st
from scipy import fftpack as f
from datetime import datetime as dt
from datetime import timedelta

f_in = "prova.txt"
#conteggio righe del file csv (escludendo header) (una riga per rilevazione)
n_rows = 0
with open(f_in, newline='') as csvfile:
    for row in csvfile.readlines()[1:]:
        n_rows = n_rows + 1
        
        
#acquisizione csv in una matrice M, con i timestamp in una list t
#schema csv: (timeStamp, Temperature, Pressure, Humidity, Wind_Speed, Wind_Direction)
i=0
M = np.zeros((n_rows,5)) # matrice dati
t = [] # vettore timestamp associati ai singoli record di M
with open(f_in,newline='') as csvfile:
    for row in csvfile.readlines()[1:]: #salto prima riga
        dummy = row.strip().split(',')
        for j in range(5):
                M[i][j] = float(dummy[j+1])
        t.append(dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S'))
        i+=1
#vettore con le velocità
v = np.float_([M[i][3] for i in range(n_rows)]) # non posso usare : per array multidimensionale

T = np.float_([M[i][0] for i in range(n_rows)]) # temperatura
p = np.float_([M[i][1] for i in range(n_rows)]) # pressione
u = np.float_([M[i][2] for i in range(n_rows)]) # umidità
d = np.float_([M[i][4] for i in range(n_rows)]) # direzione vento

# filtro di media mobile
# la convoluzione per un vettore di n pesi uguali (vettore i cui elementi sommano 1)
# restituisce la media mobile su finestre larghe n (si può ottenere una media mobile pesata con valori arbitrari dei pesi)

param_3 = 3 # ogni valore di velocità è mediato con i due adiacenti
h = 1/param_3*np.ones(param_3) # vettore dei pesi
V = np.convolve(v,h,'valid')
n_rid = int(np.size(V,axis=0))

# la convoluzione con opzione "valid" restituisce un vettore ridotto
# di lunghezza max(M, N) - min(M, N) + 1, eliminando elementi ai bordi

# si possono considerare, anzichè intervalli disgiunti, finestre sovrapposte ogni 5 minuti, es. 0-15, 5-20, 10-25... (da provare a implementare)
# noi qui dividiamo la giornata in intervalli di 15 minuti

inizio_intervalli = [0,]
minutes = t[0].minute
if minutes < 15:
    minutes = 0
elif minutes < 30:
    minutes = 15
elif minutes < 45:
    minutes = 30
else:
    minutes = 45 
t0 = t[0].replace(minute=minutes, second=0)
print(t0)
for j in range(n_rid):
    if (t[j]> t0 + timedelta(minutes=15)):
        t0 = t0 + timedelta(minutes=15)
        inizio_intervalli.append(j)
        
print(f"Numero intervalli: {len(inizio_intervalli)}")



'''
i=1
flag = True
while flag:
    t[i-1][0] = np.percentile(V[durata_int*(i-1):durata_int*i],25)
    t[i-1][1] = np.percentile(V[durata_int*(i-1):durata_int*i],50)
    t[i-1][2] = np.percentile(V[durata_int*(i-1):durata_int*i],75)
    t[i-1][3] = np.mean(V[durata_int*(i-1):durata_int*i])
    t[i-1][4] = np.sqrt(np.mean(np.power(V[durata_int*(i-1):durata_int*i],2)))
    # usare np.std per varianza
    if n-durata_int*i >= durata_int:
        i += 1
    else:
        flag = False
'''

media_raf = 0 # velocità media della raffica corrente
cont_raf = np.zeros(len(inizio_intervalli)) # contatore raffiche per ogni intervallo
int_totale = np.zeros(len(inizio_intervalli)) # intensità (media) raffiche per ogni intervallo
dur_raf = np.zeros(len(inizio_intervalli)) # durata (media) raffiche per ogni intervallo

param_1 = 1.3
param_2 = 0.85

i = 5
intervallo_corrente = 0
while i<n_rid:
    #print(f"Avanzamento: {i}/{n_rows}, intervallo_corrente = {intervallo_corrente}")
    #clear_output()
    if V[i]>param_1*np.mean(V[i-5:i-4]) and V[i]>1:
        inizio_raffica = i
        while V[i]>param_2*np.mean(V[i-3:i-1]) and i<n_rid:
            flag = 0    # va a 1 se la raffica abbraccia due intervalli, serve per inserire la raffica nell'intervallo di inizio
            #print(f"Avanzamento: {i}/{n_rows}")
            #clear_output()
            #passaggio ad un nuovo intervallo
            if intervallo_corrente < len(inizio_intervalli) - 1:
                if i == inizio_intervalli[intervallo_corrente+1]:
                    intervallo_corrente += 1 # passaggio ad un nuovo intervallo
                    flag = 1
            i += 1
        
        # aggiorno variabili
        media_raf=np.mean(V[inizio_raffica-3:i]) 
        cont_raf[intervallo_corrente - flag]+=1 # se una raffica inizia all'intervallo x e finisce a x+1, verrà contata per l'int. x+1
        int_totale[intervallo_corrente - flag]+=media_raf
        dur_raf[intervallo_corrente - flag]+=i-inizio_raffica+3

    if intervallo_corrente < len(inizio_intervalli) - 1:
        if i == inizio_intervalli[intervallo_corrente+1]:
            intervallo_corrente += 1 # passaggio ad un nuovo intervallo
    i+=1

temperature_medie, pressioni_medie, umidità_medie, direzioni_vento_medie = [], [], [], []

# Calcola intensità e durata media raffica per le finestre temporali   
i=0   
while i<len(inizio_intervalli):
    inizio = inizio_intervalli[i]
    fine = inizio_intervalli[i+1] if i<len(inizio_intervalli)-1 else len(t)

    if cont_raf[i]>=1:
        int_totale[i]=int_totale[i]/cont_raf[i]
        dur_raf[i]=dur_raf[i]/cont_raf[i]
        print(f"Intervallo {i} (prima rilevazione: {t[inizio]}, ultima rilevazione: {t[fine-1]})")
        print('Intensità media raffiche: ' + str(int_totale[i]))
        print('Durata media raffiche: ' + str(dur_raf[i]))    
        print('Contatore raffiche: ' + str(int(cont_raf[i])))
        print("\n")
    
    
    # Calcola, per ogni intervallo, media di temperatura, pressione, direzione e velocità vento
    
    temperature_medie.append(np.mean(T[inizio:fine]))
    pressioni_medie.append(np.mean(p[inizio:fine]))
    umidità_medie.append(np.mean(u[inizio:fine]))
    direzioni_vento_medie.append(np.mean(d[inizio:fine]))

    i+=1 # passo all'intervallo successivo

# relazione fra temperatura e numero delle raffiche in ogni intervallo
plt_pyplot.scatter(temperature_medie,cont_raf)
plt_pyplot.xlabel('Temperatura media')
plt_pyplot.ylabel('Contatore raffiche')
plt.show()

# da finire e rifinire