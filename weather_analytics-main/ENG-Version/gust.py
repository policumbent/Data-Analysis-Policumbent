import numpy as np
import matplotlib.pyplot as plt

class Gust:

    def __init__(self):
        self.Data = []

    def append_data(self, data):
        for datum in data:
            self.Data.append(datum)
        self.Data = np.array(self.Data)
    
    def avg_temperature(self):
        return np.mean(self.Data[:,1])
    
    def avg_pressure(self):
        return np.mean(self.Data[:,2])

    def avg_humidity(self):
        return np.mean(self.Data[:,3])
    
    def avg_speed(self):
        return np.mean(self.Data[:,4])
    
    def avg_direction(self):
        return np.mean(self.Data[:,5])
    
    def duration(self):
        return self.Data[len(self.Data)-1][0]-self.Data[0][0]

    def draw_gust(self):
        print(self.Data[0,0],self.Data[len(self.Data)-1,0])
        plt.plot_date(self.Data[:,0], self.Data[:,4])
        plt.xlabel('Time')
        plt.ylabel('Wind speed [km/h]')
        plt.show()