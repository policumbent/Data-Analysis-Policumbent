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
#ATTENZIONE! Alcuni file hanno i valori di pressione e umidità invertiti

import os
os.chdir(os.path.dirname(__file__))    #path della cartella che contiene il progetto
#print(os.getcwd())

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
import util
from interval import Interval

param_1 = 1.3
param_2 = 0.85
param_3 = 5
param_4 = 3 # amplitude interval moving avg
param_5 = 4
param_6 = 15 # amplitude of intervals

def main(file, graphs=None):

    f_in = file
    Data = util.read_file(f_in)
    
    t = Data[:,0] # timestamp
    T = Data[:,1] # temperature
    p = Data[:,2] # pressure
    u = Data[:,3] # humidity
    s = Data[:,4] # speed
    d = Data[:,5] # direction

    # se ci sono delle colonne scambiate
    p, u = u, p

    t = t[int(np.floor(param_4/2)):-int((np.floor((param_4-1)/2)))]
    T, red_len = util.moving_average(T, param_4)
    p, red_len = util.moving_average(p, param_4)
    u, red_len = util.moving_average(u, param_4)
    s, red_len = util.moving_average(s, param_4)
    d, red_len = util.moving_average(d, param_4)

    Data = np.column_stack([t,T,p,u,s,d])
    n_lines = Data.shape[0]

    # Creazione intervals
    intervals = [] 
    ts = util.first_ts(Data[0][0], param_6)
    while ts < Data[len(Data)-1][0]:
        ts_fine = ts + timedelta(minutes = param_6)
        intervals.append(Interval(ts, ts_fine))
        ts = ts_fine

    # Inserimento dati negli intervals
    j = 0
    for i in range(n_lines):
        while j < len(intervals) and not intervals[j].admits(Data[i][0]):
            j += 1
        intervals[j].insert(Data[i])

    # GRAPHS
    if "1" in graphs:
        util.find_gusts(Data, intervals, param_1, param_2, param_3, draw=True)
    else:
        util.find_gusts(Data, intervals, param_1, param_2, param_3, draw=False)
    
    if "2" in graphs:
        util.hgraph_temp_num_gusts(intervals)

    if "3" in graphs:
        util.pgraph_dir_time_speed(t, d, s, intervals)
    
    if "4" in graphs:
        util.graph_ts_TPHS(t, T, p, u, s)
        
    if "5" in graphs:
        util.graph_TPHS(T, p, u, s)
        

for file in ["../Dataset/2022_9_13_new.csv", "../Dataset/2022_9_14_new.csv", "../Dataset/2022_9_15_new.csv", "../Dataset/2022_9_16_new.csv"]:
    main(file, "5")

