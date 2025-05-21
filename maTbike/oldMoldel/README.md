# oldModel

- File analisi_teorica_cambio.m :
    Data la funzione sul tempo del vettore cadenza, presi i punti estremi dei segmenti, sono stati ricavati i relativi coefficienti di inclinazione, per poi utilizzarli per scrivere una nuova funzione che ricrea il vettore cadenza. 
    Abbiamo poi interpolato la potenza con un polinomio di grado 3 per cercare di modellarla. 
    Questi dati sono stati messi nel modello Simulink e sono una buona approssimazione dei valori originali. 

- File TestSim.slx : 
    Sono stati aggiunti i nuovi vettori ricavati di cadenza e potenza per poi modificare alcune parti del modello originale. 
    La cadenze è stata collegata alla funzione "Cambio", che è stata modificata per rilevare meglio i dati e capire quali sono le rapportature ottimali. Al posto di usare la velocità per stimare le cambiate, abbiamo utilizzato solo la cadenza da noi ricavata, tramite due nuovi coefficiente che sono:
        - "Cooldowntime" indica una sorta di stabilizzazione della cadenza (ricavato a tentativi, evita rilevazioni continue non avendo la conferma della velocità);
        - "cadence_drop_threshold" rileva una eventuale variazione significativa di cadenza (rpm).
    Se il valore di cadenza è fuori dal threshold ed è anche oltre il cooldowntime allora cambia marcia. Abbiamo fatto diverse prove andando a modificare i rapporti di trasmissione da quelli originali, sempre con metodi iterativi per cercare di incrementare la velocità finale. 

Equazioni usate \
P = vettore_potenza [ W ]\
$ \omega $  = velocità angolare $[\dfrac{rad}{s}]$ 
$$C = \dfrac{P}{\omega}$$