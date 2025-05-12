import pandas as pd
import re


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
                # Quando abbiamo latitudine e longitudine, salviamo la riga completa
                rows.append([current_time, speed, distance, lat, lon])

# Creazione del DataFrame
df = pd.DataFrame(rows, columns=["tempo", "velocità", "distanza", "latitudine", "longitudine"])


print(df)
