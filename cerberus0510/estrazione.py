import pandas as pd
import re
import matplotlib.pyplot as plt


file_path = "/Users/mario/Data-Analysis-Policumbent/cerberus0510/decodifica/dati.txt"

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

    newDf.to_csv(f'giro{n}2.csv', index=False)

