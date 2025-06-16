import matplotlib.pyplot as plt

inpFile = '/Users/mario/Data-Analysis-Policumbent/dati/cerberus/balocco/20250614/powermeter_13-06-2025@18_01_30.csv'
dati = {
    'step' : [],
    'pw' : [],
    'ipw' : [],
    'cad' : []
}

i = 0

with open(inpFile, 'r') as infile:
    line1 = infile.readline()
    for line in infile:
        linem = line.strip().split(',')
        pw = linem[1]
        pwi = linem[2]
        cad = linem[3]

        dati['step'].append(i)
        dati['pw'].append(pw)
        dati['ipw'].append(pwi)
        dati['cad'].append(cad)

        i+=1

#print(dati)

x = dati['step']
y = dati['ipw']

plt.scatter(x, y, marker='o', s=5)
plt.show()


