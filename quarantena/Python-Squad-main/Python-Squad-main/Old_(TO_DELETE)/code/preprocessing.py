'''
PREPROCESSING
'''

import os
import util
import pandas as pd
import numpy as np

# PROBLEMA: alcuni sensori potrebbero non funzionare
###################################################################
# eliminare le colonne vuote
###################################################################
def rmNullCols(df):
    df = pd.read_csv(df)
    nan_cols = [col for col in df.columns if df[col].isna().all()]
    df.drop(columns=nan_cols,inplace=True)
    # df = df.drop(columns=nan_cols)
    # return df

# PROBLEMA: alcuni sensori non sono partiti subito. 
###################################################################
# eliminare le prime (o ultime) n righe, o fino alla prima riga che abbia tutti i valori non nulli
###################################################################
def delRows(df, n=None, from_bottom=False):
    rmNullCols(df)
    # df = rmNullCols(df)
    if n is None:
        n = len(df)

    i = 0
    end = False
    while i < min(n,len(df)) and not end:
        j = 1
        nan = False
        while j < len(df.columns) and not nan:
            bottom = (len(df)-1 if from_bottom else 0)
            if np.isnan(df.iloc[0 + bottom,j]):
                df.drop(0 + bottom, inplace=True)
                nan = True
            else:
                j = j+1
        if nan == False:
            end = True
        i = i+1



###################################################################
# unire più run in uno stesso file per poter fare confronti in RapidMiner
###################################################################
folder_path = ...
df = []
#
for file in os.listdir(folder_path):
    if ".csv" in file:
        df.append(util.csv2Df(util.joinPath(folder_path, file)))

for i in range(len(df)):
    for col in df[i].columns:
        df[i] = df[i].rename(columns={col:col+str(i+1)})
df_tot = pd.concat(df, axis=1)
util.Df2csv(util.getResultsPath("all-inclusive_file.csv"), df_tot)

###################################################################
# 
###################################################################



###################################################################
# 
###################################################################

# choose a file or a folder
folder_path = ...
single_file_path = ...

# preprocessing for a single file
df = util.csv2Df(single_file_path)
delRows(df)

# same preprocessing for each file in the folder
for file in os.listdir(folder_path):
    if ".csv" in file:
        single_file_path = util.joinPath(folder_path, file)
        df = util.csv2Df(file)
        delRows(df)
