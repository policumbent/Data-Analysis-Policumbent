import numpy as np
import pandas as pd
#from datetime import datetime as dt
#from datetime import timedelta
# import matplotlib.pyplot as plt
import csv
import os

dtset_path = "../Dataset"
dtcond_path = "../Dataset/conditions/"
dtsettings_path = "../Dataset/couples/"
plot_opts_path = "../Dataset/plot_opts/"
pdfexport_path = "../Plots&Analysis/"

def moving_average(vector, filt, amplitude=3, opts='same'):
    '''moving average filter
    vector: Array
    filt: Array (filter, array of weights that add up to 1)
    amplitude: Integer (length of filt, range of the filter. Not necessary if filt is given)
    opts: String (options of the convolution; must be in ['full','valid','same'])
    
    la convoluzione per un vector di n pesi uguali (vector i cui elementi sommano a 1)
    restituisce la media mobile su finestre larghe 'amplitude' (si può ottenere una media mobile pesata con valori arbitrari dei pesi)
    '''

    if filt is None:
        filt = 1/amplitude*np.ones(amplitude)   #creation of a uniform filter
    else:
        filt_sum = sum(filt)
        if filt_sum != 1:
            for i in range(len(filt)):
                filt[i] = filt[i]/filt_sum   #normalization of the vector
        
    V = np.convolve(vector,filt,opts)
    #rd_len = int(np.size(V,axis=0))   # reduced length
    return V   #, rd_len

def readCsvFile(file_name, header=False, delimiter=','):
    '''read csv file function
    file_name: String (Path of the file)
    return: ndArray, list (header)
    '''
    data = []
    head = []
    with open(file_name,'r') as file:
        reader = csv.reader(file,delimiter=delimiter)
        #next(reader, None)
        for row in reader:
            if header == True:
                head=[str(element) for element in row]
                header = False
            else:
                data.append([element for element in row])
    return np.array(data), head

def csv2Df(file_name):
    '''
    file_name: String (Path)
    read a csv file
    return: DataFrame
    '''
    return pd.read_csv(file_name)    

def writeCsvFile(file_name, data, header):   #TODO TO BE MODIFIED
    with open(file_name,'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(header)
        for row in data:   #TO BE MODIFIED
            writer.writerow(row)
            
def Df2csv(file_name, df):
    '''
    a differenza di writeCsvFile questa funzione lascia nel csv anche l'id delle righe
    '''
    df.to_csv(file_name)

def getDatasetPath(driver_name, path_in=None, dataset_path=None):
    '''
    driver_name : String (folder name)
    path_in : String (Path) default : current
    dataset_path : String (Path)
    return Dataset Path given folder name (driver_name)
    '''
    if path_in is None:
        path_in = os.getcwd()
    if dataset_path is None:
        dataset_path = os.path.abspath(os.path.join(path_in, dtset_path))
    return os.path.join(dataset_path, driver_name).replace("\\","/")

def getCondPath(file_name):
    return os.path.abspath(os.path.join(os.getcwd(), dtcond_path+file_name)).replace("\\","/")

def getResultsPath(file_name):
    return os.path.abspath(os.path.join(os.getcwd(), pdfexport_path+file_name)).replace("\\","/")

def getSettingsPath(driver_name):
    return os.path.abspath(os.path.join(os.getcwd(), dtsettings_path+driver_name+"_settings.xlsx")).replace("\\","/")

def getPlotOptsPath():
    return os.path.abspath(os.path.join(os.getcwd(), plot_opts_path+"plot_opts.xlsx")).replace("\\","/")

def joinPath(folder_path, file_name):
    # return os.path.join(folder_path, file_name).replace("\\","/")   # meglio quello sotto
    return os.path.abspath(os.path.join(folder_path, file_name)).replace("\\","/")

def f_alpha(n, half=5):
    '''
    n : Int (number of lines in a plot)
    half : color opacity halving parameter
    generate alpha for a plot using arctan function based on n.
    half=5 means that if we have 5 lines the opacity of each is set to 0.5;
    if we have less lines the opacity is greater
    '''
    return - 1/np.pi*np.arctan(n-half) + 0.5

# def readFile(file_name):
#     '''read csv file function
#     file_name: String (Path of the file)
#     return: ndArray, header
#     '''
#     data = []
#     header = []
#     with open(file_name,'r') as file:
#         reader = csv.reader(file)
#         #next(reader, None)
#         head = True
#         for row in reader:
#             if head == True:
#                 header=[str(element) for element in row]
#                 head = False
#             else:
#                 data.append([element for element in row])
#     return np.array(data), header
