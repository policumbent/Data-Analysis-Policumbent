import csv
import pandas as pd
import numpy as np
from scipy.interpolate import pchip_interpolate
import matplotlib.pyplot as plt
from run import Config
from run import Run

def read_run(path, config_path):

    '''
    Parameters:
        path: csv file containing run
    '''

    # read config
    params = {}
    with open(config_path) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            params[row[0]] = float(row[1])

    #read data
    data = []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            data.append([float(element) for element in row])

    config = Config()
    config.set_params(params)

    run = Run(config)
    run.set_data(np.array(data))
    
    return run
