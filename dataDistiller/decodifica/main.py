import os

pathI = '../../dati/rowData/log_file'
pathO = '../../dati/rowData/txt_file'

for nf in os.listdir(pathI):
    if '.log' in nf:
        pathF = os.path.join(pathI, nf)
        nfL = nf.split('.')
        os.system(f'cat {pathF} | python3 -m cantools decode policanbent.dbc > {pathO}/{nfL[0]}.txt')
        

    
