import pandas as pd
import re
import matplotlib.pyplot as plt


file_path = "canlog_2025-05-10_pom-1.txt"

rows = []
current_time = None
speed = None
distance = None
lat = None
lon = None

# Regex patterns
time_pattern = re.compile(r"\((\d+\.\d+)\)")
speed_pattern = re.compile(r"Speed: ([\d\.]+) km/h")
distance_pattern = re.compile(r"Distance: (\d+) m")
lat_pattern = re.compile(r"Latitude: ([\d\.]+)")
lon_pattern = re.compile(r"Longitude: ([\d\.]+)")

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        time_match = time_pattern.search(line)
        if time_match:
            current_time = float(time_match.group(1))

        if "whereamiData" in line:
            continue
        if "Speed:" in line:
            match = speed_pattern.search(line)
            if match:
                speed = float(match.group(1))
        if "Distance:" in line:
            match = distance_pattern.search(line)
            if match:
                distance = int(match.group(1))
        if "Latitude:" in line:
            match = lat_pattern.search(line)
            if match:
                lat = float(match.group(1))
        if "Longitude:" in line:
            match = lon_pattern.search(line)
            if match:
                lon = float(match.group(1))
                rows.append([current_time, speed, distance, lat, lon])

# Creazione del DataFrame
df = pd.DataFrame(rows, columns=["tempo", "velocità", "distanza", "latitudine", "longitudine"])

#plt.plot(df['tempo'], df['velocità'])
#plt.show()

i = 0

for n in [1,2]:
    nRows = []

    while df['velocità'][i] < 10:
        i += 1

    while df['velocità'][i] > 10:
        nRows.append([df['tempo'][i], df['velocità'][i], df['latitudine'][i], df['longitudine'][i]])
        i += 1

    newDf = pd.DataFrame(nRows, columns=['tempo', 'velocità', 'latitudine', 'longitudine'])

    newDf.to_csv(f'giro{n}.csv', index=False)

#print(newDf)


#plt.plot(df['longitudine'], df['latitudine'], color='gray', linewidth=0.5, alpha=0.6)
'''
plt.figure(figsize=(10, 8))
sc = plt.scatter(newDf['longitudine'], newDf['latitudine'], c=newDf['velocità'], cmap='viridis', s=10)
plt.colorbar(sc, label='Velocità (km/h)')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.title('Tracciato geografico colorato per velocità')
plt.grid(True)
plt.axis('equal')
plt.show()
'''


"""from matplotlib.animation import FuncAnimation
import numpy as np


df = newDf.sort_values(by='tempo').reset_index(drop=True)

# Setup figura
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(newDf['longitudine'].min(), newDf['longitudine'].max())
ax.set_ylim(df['latitudine'].min(), newDf['latitudine'].max())
ax.set_xlabel('Longitudine')
ax.set_ylabel('Latitudine')
ax.set_title('Animazione del percorso nel tempo')
ax.set_aspect('equal')
line, = ax.plot([], [], lw=2, color='blue')  # linea animata

# Funzione di inizializzazione
def init():
    line.set_data([], [])
    return line,

# Funzione che aggiorna il grafico per ogni frame
def update(frame):
    x = df['longitudine'].iloc[:frame]
    y = df['latitudine'].iloc[:frame]
    line.set_data(x, y)
    return line,

# Crea animazione
ani = FuncAnimation(fig, update, frames=len(df), init_func=init, interval=10, blit=True)

plt.show()"""

