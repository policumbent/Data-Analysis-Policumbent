import numpy as np
from datetime import datetime as dt

class Intervallo:

    # inizio incluso, fine esclusa
    def __init__(self, ts_inizio, ts_fine):
        self.M = [] # rilevazioni
        self.R = [] # raffiche
        self.ts_inizio = ts_inizio
        self.ts_fine = ts_fine

    def ammette(self, ts):
        return ts<self.ts_fine and ts>=self.ts_inizio
    
    #inserimento ordinato (scansione dalla fine)
    def inserisci(self, ril):
        i = len(self.M) - 1
        while i >= 0 and self.M[i][0] > ril[0]:
            i -= 1
        self.M.insert(i + 1,ril)
    
    def aggiungi_raffica(self, r):
        self.R.append(r)

    def ts_prima_ril(self):
        return self.M[0]

    def ts_ultima_ril(self):
        return self.M[len(self.M)-1]

    def conteggio_raffiche(self):
        return len(self.R)

    def intensità_media_raffiche(self):
        return np.mean([r.intensità_media() for r in self.R])

    