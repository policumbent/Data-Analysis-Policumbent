# analisi cartella all_logs

NON AVVIARE IL FILE csvFile.py e logFile.py PER NESSUN MOTIVO

## file 
    - senza estensione con i log 
    - .csv
    - totale = 658


### file csv 
    d = dimensione file [byte]
    
        - d <= 38 : file vuoti o con solo intestazione (423) 64% dei file .csv e 81% dei file totali
    
    aggiunto filtro per saltare i file con valori principalmente nulli
        - a/c: rapporto tra n_righ_totali e n_righe_non_vuote

    risultano utilizzabili 31 file powermeter.csv che dovranno poi essere ancora filtrati e 30 hearthrate
    
    
    