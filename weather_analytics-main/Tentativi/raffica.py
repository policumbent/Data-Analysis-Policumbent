import numpy as np
import matplotlib.pyplot as plt

class Raffica:

    def __init__(self):
        self.rilevazioni = []

    def aggiungi_rilevazioni(self, rilevazioni):
        for ril in rilevazioni:
            self.rilevazioni.append(ril)
        self.rilevazioni = np.array(self.rilevazioni)
    
    def temperatura_media(self):
        return np.mean(self.rilevazioni[:,1])
    
    def pressione_media(self):
        return np.mean(self.rilevazioni[:,2])

    def umidita_media(self):
        return np.mean(self.rilevazioni[:,3])
    
    def intensità_media(self):
        return np.mean(self.rilevazioni[:,4])
    
    def direzione_media(self):
        return np.mean(self.rilevazioni[:,5])
    
    def durata(self):
        return self.rilevazioni[len(self.rilevazioni)-1][0]-self.rilevazioni[0][0]

    def disegna_raffica(self):
        print(self.rilevazioni[0,0],self.rilevazioni[len(self.rilevazioni)-1,0])
        plt.plot_date(self.rilevazioni[:,0], self.rilevazioni[:,4])
        plt.xlabel('Tempo')
        plt.ylabel('Intensità vento [km/h]')
        plt.show()