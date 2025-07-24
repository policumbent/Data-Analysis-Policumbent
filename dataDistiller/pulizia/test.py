import matplotlib.pyplot as plt 

file = '../../dati/cerberus/balocco/20250614/rowdata/run2/datignss.txt'

with open(file, 'r') as inf:
    dt = list()
    dtt = dict()
    for line in inf:
        print(line)
        if 'can0' in line:
            ss = inf.readline()
            if 'GbData' in ss:
                break

            print('ok')
            lL = line.strip().split()
            n = lL[0].split('.')
            i  = n[0]

            for a in range(0,2):
                inf.readline()

            cc = inf.readline()
            lll = cc.strip().split(':')
            print(lll)
            vc = int(lll[1].strip())

            if i not in dtt:
                dtt[i] = [vc]
            else:
                dtt[i].append(i)
            
            print(dtt)

print(dtt)


