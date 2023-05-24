import numpy as np
from datetime import datetime as dt
from datetime import timedelta
from gust import Gust
import matplotlib.pyplot as plt

def read_file(file_name):
    '''Acquisizione csv in una matrice Data
    Schema csv: (timeStamp, Temperature, Pressure, Humidity, Wind_Speed, Wind_Direction)
    '''
    Data = []
    with open(file_name,newline='') as csvfile:
        for line in csvfile.readlines()[1:]: #skip first line (header)
            dummy = line.strip().split(',')
            row = []
            row.append(dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S'))
            for j in range(5):
                    row.append(float(dummy[j+1]))
            Data.append(row)
    Data = np.array(Data)

    return Data

def moving_average(vector, amplitude):
    '''filtro di media mobile
    la convoluzione per un vector di n pesi uguali (vector i cui elementi sommano 1)
    restituisce la media mobile su finestre larghe 'amplitude' (si può ottenere una media mobile pesata con valori arbitrari dei pesi)
    '''

    # la convoluzione con opzione "valid" restituisce un vector ridotto
    # di lunghezza max(M, N) - min(M, N) + 1, eliminando elementi ai bordi

    w = 1/amplitude*np.ones(amplitude)   # vector dei pesi
    V = np.convolve(vector,w,'valid')
    rd_len = int(np.size(V,axis=0))   # reduced length
    return V, rd_len

def first_ts(ts, interval_amplitude):
    '''
    Restituisce il timestamp di inizio del primo interval utile (ovvero che contiene almeno una rilevazione)
    N.B. Gli intervals vengono calcolati dall'ora esatta (minutes = seconds = 0), dunque la loro amplitude dev'essere un divisore di 60
    '''
    minutes = ts.minute
    i = 0
    while minutes > i*interval_amplitude:
        i += 1
    
    minutes = (i-1)*interval_amplitude
    return ts.replace(minute=minutes, second=0)

def find_gusts(data, intervals, param_1, param_2, param_3, draw=False):

    S = data[:,4] # speed
    
    i = 5
    j = 0
    while i<len(data):

        if S[i]>param_1*np.mean(S[i-5:i-4]) and S[i]>1: # 1 è il minimo ammissibile del picco; forse da aumentare a 1.5 (da parametrizzare?)]
            gust_start = i - 3
            #print(gust_start)
            ts_start = data[i-3,0]
            while not intervals[j].admits(ts_start):
                j += 1
            while S[i]>param_2*np.mean(S[i-3:i-1]) and i<len(data) and data[i,0]-data[i-1,0]<=timedelta(seconds=param_3):
                i += 1
                #print(i)

            ts_end = data[i,0] #si può omettere
            g = Gust()
            g.append_data(data[gust_start:i, :])
            if draw is True:
                g.draw_gust()
            intervals[j].append_gust(g)
        
        i += 1
        while i<len(data) and data[i,0]-data[i-5,0]>timedelta(seconds=param_3+2):
                i+=1

def sampling_with_average(vector, amplitude):
     '''
     Riduce le dimensioni di un vector facendone la media a intervals di prefissata amplitude.
     '''
     y = []
     for i in range(len(vector)):
          if i%amplitude == 0:
               y.append(np.mean(vector[i:min(i+amplitude, len(vector))]))
     return np.array(y)

#GRAPHS
#Legend:
# h = histogram
# p = polar plot
# b = box plot
# ch = circular histogram

def hgraph_temp_num_gusts(intervals, precision=0.5):
    '''
    Istogramma con la distribuzione delle temperature medie delle gusts.
    '''
    plt.figure()

    gusts = []
    for interval in intervals:
         gusts.extend(interval.Gusts)

    x = [gust.avg_temperature() for gust in gusts] # vector con temperatura media gusts
    plt.hist(x, bins=np.arange(min(x), max(x) + precision, precision))
    plt.xticks(np.arange(min(x), max(x) + precision, precision))
    plt.xlabel('Average temperature')
    plt.ylabel('Gust count')
    plt.title('Relation : temperature - gust count (per interval)')
    plt.show()

def pgraph_dir_speed_time(t, d, s, intervals):
    plt.figure()
    d = d*2*np.pi/360 # direzioni in radianti
    ax = plt.subplot(polar=True)
    ax.set_theta_zero_location("N")
    colors = [(t[i]-t[0]).total_seconds() for i in range(1,len(t)-1)]

    plt.scatter(d,s,c=colors,cmap='Reds')
    s_max = max(s)
    plt.yticks(np.arange(s_max)+1)
    cbar = plt.colorbar(orientation="vertical",label="Intervals (time)")

    delta = (max(colors)-min(colors))/len(intervals)
    levels = [i*delta for i in range(len(intervals)+1)]
    cbar.set_ticks(levels)
    tickstr = [(t[0]+timedelta(seconds=l)).strftime("%H:%M:%S") for l in levels]
    cbar.set_ticklabels(tickstr)
    plt.title('(Wind) Direction-Speed during the day')   #Direzione-Intensità del vento nel corso della giornata
    plt.show()

def pgraph_dir_time_speed(ts, d, s, intervals):
    N = 10
    N2 = 12
    amplitude = 100
    
    plt.figure()
    d = d*2*np.pi/360 # direzioni in radianti
    ax = plt.subplot(polar=True)
    ax.set_theta_zero_location("N")
    t = [(ts[i]-ts[0]).total_seconds() for i in range(1,len(ts)-1)]

    d = sampling_with_average(d, amplitude)
    s = sampling_with_average(s, amplitude)
    t = sampling_with_average(t, amplitude)

    plt.scatter(d,t,c=s,cmap='autumn_r')

    delta = t[len(t)-1]-t[0]/N2
    yticks = [((ts[0]+timedelta(hours=i-2))-ts[0]).total_seconds() for i in range(N2)]
    plt.yticks(yticks)
    ax.set_yticklabels([(ts[0]+timedelta(seconds=yt)).strftime("%H:%M:%S") for yt in yticks])
    cbar = plt.colorbar(orientation="vertical",label="Speed")   #Intensità

    delta = (max(s)-min(s))/N
    levels = [i*delta for i in range(N+1)]
    cbar.set_ticks(levels)
    plt.title('(Wind) Direction-Speed during the day')   #Direzione-Intensità del vento nel corso della giornata
    plt.show()

def graph_ts_TPHS(t, T, p, u, s):
    plt.plot_date(t,T, markersize=1)
    plt.plot_date(t,(p-min(p))*10, markersize=1)
    plt.plot_date(t,u, markersize=1)
    plt.plot_date(t,s*10, markersize=1)
    plt.legend(["Temperature", "Pressure", "Humidity", "Speed"])
    plt.show()

def graph_TPHS(T, p, u, s):
    
    plt.plot(T, markersize=1)
    plt.plot((p-min(p))*10, markersize=1)
    plt.plot(u, markersize=1)
    plt.plot(s*10, markersize=1)
    plt.legend(["Temperature", "Pressure", "Humidity", "Speed"])
    #plt.text(-len(T)/27, (p-min(p))*10, "A")
    plt.show()
