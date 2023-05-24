#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:06:19 2022
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


#from IPython.display import clear_output
import csv
#import os
#import math
#import time
import numpy as np
import matplotlib.pylab as plab
import matplotlib.pyplot as plt
#import pywt as pwt                          #pyWavelets
import statistics as st
from scipy import fftpack as f
from datetime import datetime as dt
from datetime import timedelta
import util

param_3 = 5
param_1 = 1.3
param_2 = 0.85
param_4 = 3
param_5 = 4

#print(os.chdir("C:\\Users\\utente\\Desktop\\UNI\\TEAM_POLICUMBENT\\nuovo_codice_python")) #serve a Gab

f_in = "prova.txt"
M = util.leggi_file(f_in)
t = M[:,0]
n_rows = M.shape[0]

T = M[:,1] # temperatura
p = M[:,2] # pressione
u = M[:,3] # umidità
v = M[:,4] # non posso usare : per array multidimensionale
d = M[:,5] # direzione vento

V, n_rid = util.media_mobile(v, param_4)
T_rid, n_rid = util.media_mobile(T, param_4)
p_rid, n_rid = util.media_mobile(p, param_4)
u_rid, n_rid = util.media_mobile(u, param_4)
d_rid, n_rid = util.media_mobile(d, param_4)

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



''' # da cancellare (?)
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

medie_raf = [] # vettore delle velocità medie delle raffiche
cont_raf = np.zeros(len(inizio_intervalli)) # contatore raffiche per ogni intervallo
int_totale = np.zeros(len(inizio_intervalli)) # intensità (media) raffiche per ogni intervallo
dur_raf = np.zeros(len(inizio_intervalli)) # durata (media) raffiche per ogni intervallo


i = 5
intervallo_corrente = 0
while i<n_rid:
    #print(f"Avanzamento: {i}/{n_rows}, intervallo_corrente = {intervallo_corrente}")
    #clear_output()

    if V[i]>param_1*np.mean(V[i-5:i-4]) and V[i]>1: # 1 è il minimo ammissibile del picco; forse da aumentare a 1.5 (da parametrizzare?)
        inizio_raffica = i
        while V[i]>param_2*np.mean(V[i-3:i-1]) and i<n_rid and t[i]-t[i-1]<=timedelta(seconds=param_3): # param_3 per trattare i buchi nelle rilevazioni
            flag = 0    # va a 1 se la raffica abbraccia due intervalli, serve per inserire la raffica nell'intervallo di inizio
            #print(f"Avanzamento: {i}/{n_rows}")
            #clear_output()
            #passaggio ad un nuovo intervallo
            if intervallo_corrente < len(inizio_intervalli) - 1:
                if i >= inizio_intervalli[intervallo_corrente+1]:
                    intervallo_corrente += 1 # passaggio ad un nuovo intervallo
                    flag = 1
            i += 1
        
        #plt.figure()
        #disegna_raffica(t[inizio_raffica-3:i], V[inizio_raffica-3:i]) # intervallo da allargare

        # aggiorno variabili
        media_raf=np.mean(V[inizio_raffica-3:i]) 
        medie_raf.append(media_raf)
        cont_raf[intervallo_corrente - flag]+=1 # se una raffica inizia all'intervallo x e finisce a x+1, verrà contata per l'int. x+1
        int_totale[intervallo_corrente - flag]+=media_raf
        dur_raf[intervallo_corrente - flag]+=i-inizio_raffica+3

    if intervallo_corrente < len(inizio_intervalli) - 1:
        if i >= inizio_intervalli[intervallo_corrente+1]:
            intervallo_corrente += 1 # passaggio ad un nuovo intervallo
    if t[i]-t[i-1]>timedelta(seconds=param_3):
        i+=5
    while t[i]-t[i-5]>timedelta(seconds=param_3+2):
        i+=1
    else:
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
        print(f"1° quartile velocità vento: {np.percentile(V[inizio:fine],25)}")
        print(f"2° quartile velocità vento: {np.percentile(V[inizio:fine],50)}")
        print(f"3° quartile velocità vento: {np.percentile(V[inizio:fine],75)}")
        print("\n")
    
    
    # Calcola, per ogni intervallo, media di temperatura, pressione, direzione e velocità vento
    
    temperature_medie.append(np.mean(T[inizio:fine]))
    pressioni_medie.append(np.mean(p[inizio:fine]))
    umidità_medie.append(np.mean(u[inizio:fine]))
    direzioni_vento_medie.append(np.mean(d[inizio:fine]))

    i+=1 # passo all'intervallo successivo

# PLOTS E RAPPRESENTAZIONI :

# relazione fra temperatura e numero delle raffiche (media per intervallo)
plt.figure()
colors = np.arange(len(temperature_medie))

plt.scatter(temperature_medie,cont_raf,c=colors,cmap="YlOrRd") # provare anche Reds o plasma_r (reversed)  (in gen. vedi "choosing colormaps in Matplotlib")
#plt.cm. # consultare la tendina proposta per suggerimenti sulle colormaps
cbar = plt.colorbar(orientation="vertical",label="Intervalli")
cbar.set_ticks(np.arange(len(inizio_intervalli)))
tickstr = [t[i].strftime("%H:%M") for i in inizio_intervalli]
cbar.set_ticklabels(tickstr)
plt.xlabel('Temperatura media')
plt.ylabel('Contatore raffiche')
plt.title('Relazione temperatura - numero raffiche (per intervallo)')
plt.show()
'''
# relazione fra temperatura e numero delle raffiche
# idea : se due intervalli, anche lontani, hanno temperatura molto simile, ha senso fare la media delle raffiche dei due e rappresentare quel valore per un unico valore di temperatura
# in questo caso si è scelto di considerare intervalli di temperatura di ampiezza k (se k è piccolo si ottiene lo stesso grafico di sopra)
temp_med = np.array(temperature_medie)
indici_notnan = np.logical_not(np.isnan(temp_med))
temp_med = temp_med[indici_notnan] # elimino i NaN
cont_raf_ar = np.array(cont_raf)
cont_raf_sort = cont_raf_ar[indici_notnan] # elimino i dati corrispondenti ai NaN nei valori di temperatura

# istogramma temperatura-numero raffiche (per intervallo)
temp_med_new = []
for i in np.arange(len(temp_med)) :
    for j in np.arange(cont_raf_ar[i]) :
        temp_med_new.append(temp_med[i])
plt.figure()
#bins = 20
plt.hist(temp_med_new) #,bins)
plt.title('Relazione temperatura - numero raffiche (per intervallo)')
plt.show()

temp_med_sort = sorted(temp_med) # ordino i dati
cont_raf_sort = cont_raf_sort[np.argsort(temp_med)] # ordino il contatore delle raffiche come il vettore di temperature (per avere corrispondenza)
temp_min = temp_med_sort[0]
temp_med_sort_new = []
cont_raf_sort_new = []
i = 0
j = -1
dk = 0.5 # provare anche 0.5 o qualsiasi altro valore (differenza minima tra le temperature rappresentate -> precisione)
k = dk
flag = 1 # nuovo intervallo
n_int = 0
# raggruppo le raffiche di diversi intervalli in un unico contatore, se cadono nello stesso intervallo di temperatura di ampiezza k
while i < len(temp_med_sort) :
    if temp_med_sort[i] < (temp_min)+k : # provare anche 'math.ceil(temp_min)+k' o round()
        if flag == 1 :
            flag = 0
            temp_med_sort_new.append((temp_min)+k) # provare anche 'math.ceil(temp_min)+k' o round()
            cont_raf_sort_new.append(0)
            if j >= 0 :
                cont_raf_sort_new[j] = cont_raf_sort_new[j]/n_int
                n_int = 0
            j+=1

        cont_raf_sort_new[j]+=cont_raf_sort[i]
        n_int+=1
        if i == len(temp_med_sort)-1 :
            cont_raf_sort_new[j] = cont_raf_sort_new[j]/n_int
        i+=1
    else :
        flag = 1
        k+=dk

plt.figure()
plt.scatter(temp_med_sort_new,cont_raf_sort_new)
plt.xlabel('Temperatura media')
plt.ylabel('Contatore raffiche')
plt.title('Relazione temperatura - numero raffiche')
plt.show()
# stesso grafico ma tramite step chart
plt.figure()
plt.step(temp_med_sort_new,cont_raf_sort_new)
plt.xlabel('Temperatura media')
plt.ylabel('Contatore raffiche')
plt.title('Relazione temperatura - numero raffiche')
plt.show()

# istogramma temperatura-numero raffiche
# non buono nella parte finale, accorpa troppe raffiche -> occorre aumentare molto bins per un risultato buono
temp_med_new = []
for i in np.arange(len(temp_med_sort_new)) :
    for j in np.arange(cont_raf_sort_new[i]) :
        temp_med_new.append(temp_med_sort_new[i])
plt.figure()
bins = 50
plt.hist(temp_med_new,bins)
plt.title('Relazione temperatura - numero raffiche')
plt.show()
'''

# distribuzione dell'intensità delle raffiche nella giornata
plt.figure()
plt.plot_date([t[i] for i in inizio_intervalli],int_totale)
plt.xlabel('Intervallo')
plt.ylabel('Intensità media raffiche')
plt.title('Intensità raffiche nel corso della giornata')
plt.show()

# quartili velocità raffiche nella giornata
medie_raf = np.array(medie_raf)
print(f"1° quartile velocità raffiche: {np.percentile(medie_raf,25)}")
print(f"2° quartile velocità raffiche: {np.percentile(medie_raf,50)}")
print(f"3° quartile velocità raffiche: {np.percentile(medie_raf,75)}")

# da aggiungere varianza, anche per intervallo

# boxplot dell' intensità delle raffiche nella giornata
plt.figure()
plt.boxplot(medie_raf)
plt.ylabel('Intensità media raffiche')
plt.title('Intensità raffiche nel corso della giornata')
plt.show()

# direzione del vento durante la giornata
plt.figure()
plt.plot_date(t[:],d[:])
plt.ylabel('Direzione vento')
plt.title('Direzione del vento nel corso della giornata')
plt.show()

# polar plot direzione e intensità vento, colormap per il tempo
# RICORDA di invertire -> senso orario invece di antiorario
plt.figure()
dd = d_rid*2*np.pi/360
ax = plt.subplot(polar=True)
ax.set_theta_zero_location("N")
colors = np.arange(len(dd))
plt.scatter(dd,V,c=colors,cmap='Reds')
v_max = max(V)
plt.yticks(np.arange(v_max)+1)
cbar = plt.colorbar(orientation="vertical",label="Intervalli")
cbar.set_ticks(np.array(inizio_intervalli))
tickstr = [t[i].strftime("%H:%M") for i in inizio_intervalli]
cbar.set_ticklabels(tickstr)
plt.title('Direzione-Intensità del vento nel corso della giornata')
plt.savefig("direzione-intensità vento")

plt.figure()
dd = d_rid*2*np.pi/360
ax = plt.subplot(polar=True)
ax.set_theta_zero_location("N")
colors = V
plt.scatter(dd,np.arange(len(dd)),c=V, cmap='Reds')
v_max = max(V)
plt.yticks(inizio_intervalli)
cbar = plt.colorbar(orientation="vertical",label="Intervalli")
cbar.set_ticks(np.array(inizio_intervalli))
tickstr = [t[i].strftime("%H:%M") for i in inizio_intervalli]
cbar.set_ticklabels(tickstr)
plt.title('Direzione-Intensità del vento nel corso della giornata')
plt.savefig("direzione-intensità vento 2")