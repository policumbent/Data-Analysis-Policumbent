import numpy as np
from datetime import datetime as dt

class Interval:

    # inizio incluso, fine esclusa
    def __init__(self, ts_begin, ts_end):
        self.Data = []
        self.Gusts = []
        self.ts_begin = ts_begin
        self.ts_end = ts_end

    def admits(self, ts):
        return ts<self.ts_end and ts>=self.ts_begin
    
    #inserimento ordinato (scansione dalla fine)
    def insert(self, datum):
        i = len(self.Data) - 1
        while i >= 0 and self.Data[i][0] > datum[0]:
            i -= 1
        self.Data.insert(i + 1,datum)
    
    def append_gust(self, gust):
        self.Gusts.append(gust)

    def ts_first_datum(self):
        return self.Data[0]

    def ts_last_datum(self):
        return self.Data[len(self.Data)-1]

    def gust_count(self):
        return len(self.Gusts)

    def avg_gust_speed(self):
        return np.mean([gust.avg_speed() for gust in self.Gusts])
