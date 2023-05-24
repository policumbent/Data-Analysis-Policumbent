from datetime import datetime as dt
from datetime import timedelta
import os
import numpy as np

def preprocessing(f_in, f_out):

    f = open(f_out, "w")

    ts_riga_prec = None
    n = 0
    acc = np.zeros(5)
    nuovo_secondo = False
    prima_riga = True

    i = 0
    with open(f_in, newline='') as csvfile:
        for row in csvfile.readlines()[:]:

            dummy = row.strip().split(',')

            #Se il file csv ha, nell'ultimo attributo, due valori invece che uno, separati da spazio: prendiamo il primo,
            #eliminiamo l'ultimo
            if i>0:   
                dummy[5] = dummy[5].strip().split(' ')[0]       

            ###Scrittura riga
            #controllo se la data è valida
            try:
                res = bool(dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S'))
            except ValueError:
                res = False

            if i == 1:
                if res == False:
                    raise ValueError("Incorrect data format, should be YYYY/MM/DD HH:MM:SS") # se il primo timestamp è sbagliato lo devo eliminare manualmente
                primo_timestamp = dt.strptime(dummy[0], '%Y/%m/%d %H:%M:%S') #salvo la data del file
            if i == 0:
                stringa = dummy[0] + ',' + dummy[1] + ',' + dummy[2] + ',' + dummy[3] + ',' + dummy[4] + ',' + dummy[5]
                f.write(stringa)
            elif res == True:
                if dt.strptime(dummy[0],'%Y/%m/%d %H:%M:%S') - primo_timestamp < timedelta(days=1):
                    if ts_riga_prec is not None and dummy[0] != ts_riga_prec:
                        nuovo_secondo = True
                        n = 1
                        for j in range(5):
                            acc[j] = float(dummy[j+1])
                    if not nuovo_secondo:
                        n += 1
                        for j in range(5):
                            acc[j] += float(dummy[j+1])

                    if nuovo_secondo == True:  #Elimino errori (giorni diversi) 
                        acc = acc/n
                        stringa = dummy[0] + ', ' + str(acc[0]) + ', ' + str(acc[1]) + ', ' + str(acc[2]) + ', ' + str(acc[3]) + ', ' + str(acc[4])
                        f.write("\n" + stringa)
                        nuovo_secondo = False
                        prima_riga = False
                    ts_riga_prec = dummy[0]

            i+=1


    f.close()

    '''n_rows = 0
    # evidenzia problemi di "buchi" nelle rilevazioni
    with open(f_out, newline='') as csvfile:
        for row in csvfile.readlines()[1:]:
            n_rows+=1
    i = 0
    with open(f_out, newline='') as csvfile:
        for row in csvfile.readlines()[1:]:
            i+=1
            if (i == 1):
                primo_timestamp = dt.strptime(row.split(',')[0], '%Y/%m/%d %H:%M:%S')
            if (i == n_rows):
                ultimo_timestamp = dt.strptime(row.split(',')[0], '%Y/%m/%d %H:%M:%S')

    n_rilev_s = 1 # rilevazioni al secondo
    delta_time_tot = ultimo_timestamp - primo_timestamp
    print(f"Rilevazioni teoriche considerandone una al secondo (Differenza di timestamp tra la prima e l'ultima rilevazione): {delta_time_tot.seconds*n_rilev_s}")
    print(f"Rilevazioni effettuate: {n_rows}")'''

def accorpamento_file(file_input, file_output):
    '''
    File_input: lista di percorsi dei file da accorpare
    File_output: percorso file output
    '''

    header = True
    f = open(file_output, "w")
    for file in file_input:
        with open(file) as csvfile:
            for row in csvfile.readlines()[0 if header else 1:]:
                f.write(row)
                header = False

os.chdir("C:\\Users\\andre\\Dropbox (Politecnico Di Torino Studenti)\\Policumbent\\Dataset")
accorpamento_file(["2022_9_13__17_15_0.csv", "2022_9_13__22_15_13.csv"], "2022_9_13.csv")
accorpamento_file(["2022_9_15__12_50_55.csv", "2022_9_15__13_11_47.csv", "2022_9_15__13_54_12.csv", "2022_9_15__13_55_4.csv", "2022_9_15__14_8_3.csv", "2022_9_15__15_52_56.csv"], "2022_9_15.csv")
accorpamento_file(["2022_9_16__12_33_18.csv", "2022_9_16__12_57_25.csv", "2022_9_16__13_1_13.csv", "2022_9_16__13_20_57.csv", "2022_9_16__15_12_51.csv", "2022_9_16__15_17_2.csv"], "2022_9_16.csv")
preprocessing("2022_9_13.csv", "2022_9_13_new.csv")
preprocessing("2022_9_14__7_52_58.csv", "2022_9_14_new.csv")
preprocessing("2022_9_15.csv", "2022_9_15_new.csv")
preprocessing("2022_9_16.csv", "2022_9_16_new.csv")
#preprocessing("prova.csv", "prova2.csv")