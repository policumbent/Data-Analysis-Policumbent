import os
import shutil

src_path  = '/Users/mario/Data-Analysis-Policumbent/dati/logsVari/rowLogs'
dstCsv_path = '/Users/mario/Data-Analysis-Policumbent/dati/logsVari/csv_file'

s = 38
i = 0
e = 0
t = 0
b = 0

for nome_file in os.listdir(src_path):
    t += 1
    percorso_file = os.path.join(src_path, nome_file)
    #print(nome_file,i)

    if os.path.isfile(percorso_file):
        dimensione = os.path.getsize(percorso_file)
        #print(dimensione)

    if nome_file.endswith('.csv'):
        i +=1
        if dimensione <= s:
            e += 1
            with open(percorso_file, 'r') as infile:
                #line1 = infile.readline()
                for line in infile:
                    b += 1
                
                #print(b)
                b = 0
            
        else:
            with open(percorso_file, 'r') as infile:
                a = 0
                c = 0
                line1 = infile.readline()
                for line in infile:
                    c += 1
                    lLine = line.strip().split(',')
                    if len(lLine) >= 2:
                        if lLine[1] != '0.0':
                            a += 1
                            #print(lLine)
                
                if a/c > 0.1:
                    nm = nome_file.split('-')
                    #print(nm)
                    if 'powermeter' in nm[0]:
                        #print(nome_file, 'power')
                        dst = os.path.join(dstCsv_path, 'powermeter')
                    
                    elif 'hearthrate' in nm[0]:
                        #print(nome_file, 'heart')
                        dst = os.path.join(dstCsv_path, 'hearthrate')


                    #print(nome_file)
                    #print(c, a, a/c)

                    dstF = os.path.join(dst, nome_file)
                    print(percorso_file, dstF)
                    shutil.copy2(percorso_file, dstF)
                    print(f"Spostato: {nome_file}")
            

#print(t, i, e, e/t, e/i)
