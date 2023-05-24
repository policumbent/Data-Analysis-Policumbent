from datetime import datetime as dt

f_out = "zzz.txt" # file corretto
f_in = "2022_9_13__17_15_0.csv" # file input

f = open(f_out, "w")


i = 0
with open(f_in, newline='') as csvfile:
    for row in csvfile.readlines()[:]:

        dummy = row.split(',')

        #salvo la data del file
        if i == 1:
            primo_timestamp = dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S')

        #Se il file csv ha, nell'ultimo attributo, due valori invece che uno, separati da spazio: prendiamo il primo,
        #eliminiamo l'ultimo
        if i>0:   
            dummy[5] = dummy[5].strip().split(' ')[0]
        str = dummy[0] + ',' + dummy[1] + "," + dummy[2] + ',' + dummy[3] + ',' + dummy[4] + ',' + " " + dummy[5]

        print(dummy[0])
        # Scrittura riga
        if i == 0:
            f.write(str)
        elif dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S').date == primo_timestamp:  #Elimino errori (date sballate)
            f.write(str + "\n")

        i = i + 1


f.close()

# evidenzia problemi di "buchi" nelle rilevazioni
with open(f_out, newline='') as csvfile:
    for row in csvfile.readlines()[1:]:
        n_rows = n_rows + 1
        
with open(f_out, newline='') as csvfile:
    for row in csvfile.readlines()[1:]:        
        if (row == 1):
            primo_timestamp = dt.strptime(row.split(',')[0], '%Y/%m/%d %H:%M:%S')
        if (row == n_rows)
            ultimo_timestamp = dt.strptime(row.split(',')[0], '%Y/%m/%d %H:%M:%S')

n_rilev_s = 1 # rilevazioni al secondo
delta_time_tot = ultimo_timestamp-primo_timestamp
print(f"Rilevazioni teoriche considerandone una al secondo (Differenza di timestamp tra la prima e l'ultima rilevazione): {delta_time_tot*n_rilev_s}")
print(f"Rilevazioni effettuate: {n_rows}")