import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def normalizza(path):
    df = pd.read_csv(path)
    newDf = df[['timestamp', 'rxShifting', 'raw_distance', 'raw_speed', 'latitude', 'longitude', 'heartRate', 'power', 'cadence']].copy()
    for col in newDf.columns:
        newDf.loc[:,col] = newDf[col].replace(0, np.NaN)
    
    colRules = {
            'rxShifting' : 'first',
            'raw_speed' : 'mean',
            'raw_distance' : 'mean',
            'latitude' : 'mean',
            'longitude' : 'mean',
            'heartRate' : 'mean',
            'power' : 'mean',
            'cadence' : 'mean'
        }
    
    newDf["timestamp"] = pd.to_datetime(newDf["timestamp"], errors="coerce")
    #newDf['timestamp'] = newDf['timestamp'].dt.time
    newDf['second'] = newDf['timestamp'].dt.floor('S')
    normDf = newDf.groupby('second', as_index = False).agg(colRules)
    normDf = normDf.rename(columns={'second' : 'timestamp'})

    normDf.to_csv(f'../../dati/Cerberus/balocco/20250913/test.csv',index=False)

    

    

def main():
    pathI = '../../dati/Cerberus/balocco/20250913/2025-09-13T10_26_14+0200.csv'
    pathO = pathI #specificare se differente

    dir = False

    if dir:
        pass

    else:
        normalizza(pathI)


main()