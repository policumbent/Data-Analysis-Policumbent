# __DataDistiller__

## Obiettivo
sviluppo di un softwer per la pulizia e l'analisi dei dati provenienti da powermeter, cardiofrequenzimetro e gps che sia di facile utilizzo per tutti i membri del team durante i test e le gare.

## Cosa deve Fare 
ipotiziamo che i file siano stati caricati in una cartella rowdata

1. __controllo e smistamento__: le estensioni presenti dovrebbero essere .csv per i dati di powermeter e cardiofrequenzimetro e .log per quelli dal gns.\
(i log del gns spesso non hanno estensione)
    1. __aggiungere__ estensione .log (se non presente)
    2. __decodificare__ i log del gns e esportarli in file.txt
    3. __dividere__ i file per sensore
        1. __Powermeter__
        2. __Cardiofrequenzimetro__
        3. __Gns__ (dividendo .log e .txt)
        
        (non sempre sono presenti i dati di tutti i sensori)
2. __pulizia__
3. __normalizzazione__
4. __unione__
5. __analisi__
    

