import os
import shutil


pathI = '../../dati/rowData/rowLogs'
pathO = '../../dati/rowData/log_file'

for fn in os.listdir(pathI):
    if not fn.endswith('.csv') and not fn.endswith('.md'):
        pathFile = os.path.join(pathI, fn)
        dim = os.path.getsize(pathFile)
        #print(dim)
        if dim > 0:
            fnL = f'{fn}.log'
            pathNfile = os.path.join(pathO, fnL)
            shutil.copy2(pathFile, pathNfile)
            
            