import numpy as np
from datetime import datetime as dt
from datetime import timedelta
from raffica import Raffica
import matplotlib.pyplot as plt
# import intervalli?

def leggi_file(nome_file):
    '''Acquisizione csv in una matrice M
    Schema csv: (timeStamp, Temperature, Pressure, Humidity, Wind_Speed, Wind_Direction)
    '''
    M = []
    with open(nome_file,newline='') as csvfile:
        for row in csvfile.readlines()[1:]: #salto prima riga
            dummy = row.strip().split(',')
            riga = []
            riga.append(dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S'))
            for j in range(5):
                    riga.append(float(dummy[j+1]))
            M.append(riga)
    M = np.array(M)

    return M

def media_mobile(vettore, ampiezza):
    '''filtro di media mobile
    la convoluzione per un vettore di n pesi uguali (vettore i cui elementi sommano 1)
    restituisce la media mobile su finestre larghe 'ampiezza' (si può ottenere una media mobile pesata con valori arbitrari dei pesi)
    '''

    # la convoluzione con opzione "valid" restituisce un vettore ridotto
    # di lunghezza max(M, N) - min(M, N) + 1, eliminando elementi ai bordi

    h = 1/ampiezza*np.ones(ampiezza) # vettore dei pesi
    V = np.convolve(vettore,h,'valid')
    n_rid = int(np.size(V,axis=0))
    return V, n_rid

def primo_ts(ts, ampiezza_intervalli):
    '''
    Ampiezza intervalli dev'essere divisore di 60
    '''
    minutes = ts.minute
    i = 0
    while minutes > i*ampiezza_intervalli:
        i += 1
    
    minutes = (i-1)*ampiezza_intervalli
    return ts.replace(minute=minutes, second=0)

def trova_raffiche(rilevazioni, intervalli, param_1, param_2, param_3, disegna=False):

    V = rilevazioni[:,4] # velocità
    
    i = 5
    j = 0
    while i<len(rilevazioni):

        if V[i]>param_1*np.mean(V[i-5:i-4]) and V[i]>1: # 1 è il minimo ammissibile del picco; forse da aumentare a 1.5 (da parametrizzare?)]
            inizio_raffica = i - 3
            #print(inizio_raffica)
            ts_inizio = rilevazioni[i-3,0]
            while not intervalli[j].ammette(ts_inizio):
                j += 1
            while V[i]>param_2*np.mean(V[i-3:i-1]) and i<len(rilevazioni) and rilevazioni[i,0]-rilevazioni[i-1,0]<=timedelta(seconds=param_3):
                i += 1
                #print(i)

            ts_fine = rilevazioni[i,0]
            r = Raffica()
            r.aggiungi_rilevazioni(rilevazioni[inizio_raffica:i, :])
            if disegna is True:
                r.disegna_raffica()
            intervalli[j].aggiungi_raffica(r)
        
        i += 1
        while i<len(rilevazioni) and rilevazioni[i,0]-rilevazioni[i-5,0]>timedelta(seconds=param_3+2):
                i+=1

def campionamento_con_media(vettore, ampiezza):
     '''
     Riduce le dimensioni di un vettore facendone la media a intervalli di prefissata ampiezza.
     '''
     y = []
     for i in range(len(vettore)):
          if i%ampiezza == 0:
               y.append(np.mean(vettore[i:min(i+ampiezza, len(vettore))]))
     return np.array(y)

def temp_num_raff(intervalli, precisione=0.5):
    '''
    Istogramma con la distribuzione delle temperature medie delle raffiche.
    '''
    plt.figure()

    raffiche = []
    for intervallo in intervalli:
         raffiche.extend(intervallo.R)

    x = [raffica.temperatura_media() for raffica in raffiche] # vettore con temperatura media raffiche
    plt.hist(x, bins=np.arange(min(x), max(x) + precisione, precisione))
    plt.xticks(np.arange(min(x), max(x) + precisione, precisione))
    plt.xlabel('Temperatura media')
    plt.ylabel('Contatore raffiche')
    plt.title('Relazione temperatura - numero raffiche (per intervallo)')
    plt.show()

def direzione_intensita_tempo(t, d, v, intervalli):
    plt.figure()
    d = d*2*np.pi/360 # direzioni in radianti
    ax = plt.subplot(polar=True)
    ax.set_theta_zero_location("N")
    colors = [(t[i]-t[0]).total_seconds() for i in range(1,len(t)-1)]

    plt.scatter(d,v,c=colors,cmap='Reds')
    v_max = max(v)
    plt.yticks(np.arange(v_max)+1)
    cbar = plt.colorbar(orientation="vertical",label="Intervalli")

    delta = (max(colors)-min(colors))/len(intervalli)
    altezze = [i*delta for i in range(len(intervalli)+1)]
    cbar.set_ticks(altezze)
    tickstr = [(t[0]+timedelta(seconds=a)).strftime("%H:%M:%S") for a in altezze]
    cbar.set_ticklabels(tickstr)
    plt.title('Direzione-Intensità del vento nel corso della giornata')
    plt.show()

def direzione_tempo_intensita(ts, d, v, intervalli):
    N = 10
    N2 = 12
    ampiezza = 100
    
    plt.figure()
    d = d*2*np.pi/360 # direzioni in radianti
    ax = plt.subplot(polar=True)
    ax.set_theta_zero_location("N")
    t = [(ts[i]-ts[0]).total_seconds() for i in range(1,len(ts)-1)]

    d = campionamento_con_media(d, ampiezza)
    v = campionamento_con_media(v, ampiezza)
    t = campionamento_con_media(t, ampiezza)

    plt.scatter(d,t,c=v,cmap='Reds')

    delta = t[len(t)-1]-t[0]/N2
    yticks = [((ts[0]+timedelta(hours=i-2))-ts[0]).total_seconds() for i in range(N2)]
    plt.yticks(yticks)
    ax.set_yticklabels([(ts[0]+timedelta(seconds=yt)).strftime("%H:%M:%S") for yt in yticks])
    cbar = plt.colorbar(orientation="vertical",label="Intensità")

    delta = (max(v)-min(v))/N
    altezze = [i*delta for i in range(N+1)]
    cbar.set_ticks(altezze)
    plt.title('Direzione-Intensità del vento nel corso della giornata')
    plt.show()

