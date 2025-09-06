import os


def decodifica(pathI, pathO):
    for nf in os.listdir(pathI):
        if '.log' in nf:
            pathF = os.path.join(pathI, nf)
            nfL = nf.split('.')
            os.system(f'cat {pathF} | python3 -m cantools decode policanbent.dbc > {pathO}/{nfL[0]}.txt')


def aggEstensione(path):
      for nf in os.listdir(path):
        pathFl = os.path.join(path, nf)

        if os.path.isfile(pathFl):
            nf, ext = os.path.splitext(pathFl)
            if not ext:
                newnf = f'{nf}.log'
                os.rename(pathFl, newnf)

    
def main():
    pathI = '../../dati/Cerberus/stupinigi/20250906/rowdata'
    pathO = pathI  # se path in != path out specificarla

    estensione = True

    if estensione:
        aggEstensione(pathI)
    
    decodifica(pathI, pathO)


main()