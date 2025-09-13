import pandas as pd
import matplotlib.pyplot as plt
import os


def accoppia(df, n0):
    path = '../../dati/rowData/csv_file/hearthrate'
    
    pR = df['timestamp'].head(1).iloc[0]
    print(pR)

    n1 = n0.strip().split('@')
    n2 = n1[0].split('_')

    for nf in os.listdir(path):
        #if n2[1] in nf:
        pathF = os.path.join(path, nf)
        dfh = pd.read_csv(pathF)
        dfh['timestamp'] = pd.to_datetime(dfh['timestamp'])
        print(dfh)
        if pR in dfh['timestamp'].values:
            print(nf)


def byDir(path):
    for nf in os.listdir(path):
        if '.csv' in nf:
            pathF = os.path.join(path, nf)

            print(nf)

            df = pd.read_csv(pathF)
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            ndf = normalizza(df, True)

            accoppia(ndf, nf)



            break


def searchData(nf, T):
    if T:
        dt, r = nf.split('T')
        rr = r.split('+')
        data = f'{dt} {rr[0][0:2]}:{rr[0][2:4]}:{rr[0][4:6]}'
    
    else:
        dt, r = nf.split('@')
        d = dt.split('_')
        dd = d[1].split('-')
        data = f'{dd[2]}-{dd[1]}-{dd[0]} {r[0:2]}:{r[2:4]}:{r[4:6]}'

    
    return data


def normGnss(pathI):
    globalDf = pd.DataFrame()
    for nf in os.listdir(pathI):
        pathF = os.path.join(pathI, nf)
        df = pd.read_csv(pathF)

        start_time = pd.to_datetime(searchData(nf, True))
        df["timestamp"] = start_time + pd.to_timedelta(df["timestamp"], unit="s")

        colRules = {
            'tkBattery' : 'mean',
            'rxShifting' : 'first',
            'gear' : 'first',
            'speed' : 'mean',
            'distance' : 'mean',
            'raw_speed' : 'mean',
            'raw_distance' : 'mean',
            'latitude' : 'mean',
            'longitude' : 'mean'
        }

        rules = dict()

        for c in df.columns:
            if c in colRules:
                rules[c] = colRules[c]
            
        normDf = normalizza(df, rules)

        globalDf = pd.concat([globalDf, normDf], ignore_index=False)
        globalDf = globalDf.fillna(0)
    
    globalDf = globalDf.sort_values(by='timestamp').reset_index(drop=True)
    print(globalDf)

    return globalDf


def normPowerm(pathI):
    globalDf = pd.DataFrame()
    for nf in os.listdir(pathI):
        pathF = os.path.join(pathI, nf)
        print(nf)

        df = pd.read_csv(pathF)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        colRules = {
            'power' : 'mean',
            'instant_power' : 'mean',
            'cadence' : 'mean'
        }

        normDf = normalizza(df, colRules)
        print(normDf)
        normDf['timestamp'] = pd.date_range(start=searchData(nf, False), periods = len(normDf), freq='S')

        print(normDf)

        globalDf = pd.concat([globalDf, normDf], ignore_index=False)
        globalDf = globalDf.fillna(0)
    
    globalDf = globalDf.sort_values(by='timestamp').reset_index(drop=True)
    print(globalDf)

    return globalDf


def normalizza(df, rules):
    df["second"] = df["timestamp"].dt.floor("S")
    normDf = df.groupby('second', as_index = False).agg(rules)
    normDf = normDf.rename(columns={'second' : 'timestamp'})
    
    return normDf


def main():

    pathI = '../../dati/Cerberus/stupinigi/20250906/rowdata'
    pathO = '../../dati/Cerberus/stupinigi/20250906'

    for dir in os.listdir(pathI):
        if dir == 'powermeter':
            newPath = os.path.join(pathI, dir)

            dfp = normPowerm(newPath)

        elif dir == 'gnss':
            newPath = os.path.join(pathI, dir)
            for nDir in os.listdir(newPath):
                if nDir == 'csv_file':
                    newNpath = os.path.join(newPath, nDir)

                    dfG = normGnss(newNpath)
    
    mergeDf = pd.merge(dfp, dfG, on='timestamp', how='inner')

    pathC = os.path.join(pathO, 'merge.csv')
    mergeDf.to_csv(pathC, index=False)


main()
