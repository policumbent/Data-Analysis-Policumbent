import csv
import pandas as pd
import numpy as np
from scipy.interpolate import pchip_interpolate
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
    
class Run:
    def __init__(self, config):
        self.config = config
    
    def set_data(self, data):
        

        self.data = pd.DataFrame(data, columns=["Time", "Torq", "Speed", "Power", "Distance", "Cadence", "Heart rate", "ID", "Altitude"])
        self.data["Time"] = pd.Series([dt.datetime(year=2000,month=1,day=1,minute=round(np.floor(t)), second=round((t-np.floor(t))*60)) for t in self.data["Time"]]) # convert times into dt.time
        self.data["Speed"]=self.data["Speed"]/3.6
        self.data["Torq"]=self.data["Power"]*60/self.data["Cadence"] # wheel or pedal rpm? (here pedal)
        self.data["Wheel rpm"]=self.data["Cadence"] # TODO, they will give it to us
        self.data["Distance"]=self.data["Distance"]
        n = len(self.data)
        self.data["Wind"] = np.zeros(n) # TODO: wind speed for each measurement
        self.data["Theta"] = np.zeros(n) # TODO: wind direction for each measurement
        self.v_cr = np.array([0,30,45,55,70,90,105,120,130,140,150])/3.6
        self.cr = np.array([0.0027,0.0030,0.0032,0.0033,0.0035,0.0037,0.0038,0.0040,0.0040,0.0041,0.0041])
        self.v_cd = np.hstack((np.arange(30,110,10),np.arange(105,155,5)))
        self.cd_CFD = [0.04047,0.03601,0.03308,0.03102,0.02973,0.03069,0.03548,0.03758,0.03778,0.03792,0.03817,0.03852,0.03901,0.03986,0.04076,0.04097,0.04120,0.04124]

    def plot_cd_CFD(self):
        plt.plot(self.v_cd, self.cd_CFD, label="Cd CFD")
        plt.legend()
        plt.show()

    def plot_profiles(self, abscissa="time"):
        xformatter = mdates.DateFormatter('%M:%S')
        x = self.data["Distance"] if abscissa=="space" else self.data["Time"]
        plt.plot(x,self.data["Speed"]*3.6, label="Speed (km/h)", markersize=1)
        plt.plot(x,self.data["Power"], label="Power", markersize=1)
        plt.plot(x,self.data["Cadence"], label="Cadence", markersize=1)
        plt.plot(x,self.data["Torq"], label="Torq", markersize=1)

        if abscissa != "space":
            plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        plt.legend()
        plt.show()
        delta_t = [(t2-t1).total_seconds() for t2,t1 in zip(self.data["Time"][1:], self.data["Time"][:-1])]
        plt.plot(x,(self.data["Speed"][1:]-self.data["Speed"][:-1])/delta_t)
        plt.title("Acceleration (ms^-2)")
        plt.show()

    def plot_speed_loss(self):
        x = self.data["Time"]
        plt.plot(x,self.data["Wheel rpm"]*self.config.get("Radius"), label="Theoretical speed")
        plt.plot(x,self.data["Speed"], label="Measured speed")
        plt.plot(x,self.data["Wheel rpm"]*self.config.get("Radius")-self.data["Speed"], label="Difference")
        plt.title("Speed loss")
        plt.legend()
        plt.show()
        
    
        
class Config:
    def set_params(self, dictionary):
        self.params = dictionary

    def get(self, param_name):
        return self.params[param_name]

