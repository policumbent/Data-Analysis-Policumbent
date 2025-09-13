import os
import re
import pandas as pd


# Timestamp
time_pattern = re.compile(r"\((\d+\.\d+)\)")

# Speed e Distance
speed_pattern = re.compile(r"Speed:\s*([\d\.]+)\s*km/h")
distance_pattern = re.compile(r"Distance:\s*(\d+)\s*m")

# RawSpeed e RawDistance
raw_speed_pattern = re.compile(r"RawSpeed:\s*([\d\.]+)\s*km/h")
raw_distance_pattern = re.compile(r"RawDistance:\s*(\d+)\s*m")

# Latitude e Longitude 
lat_pattern = re.compile(r"Latitude:\s*([\d\.]+)")
lon_pattern = re.compile(r"Longitude:\s*([\d\.]+)")

# Gear
gear_pattern = re.compile(r"GbGear:\s*(\d+)")

# TelekBattery
tk_battery = re.compile(r"TelekBattery:\s*(\d+)\s*%")

# RxShifting
rxShifting = re.compile(r"RxShifting:\s*(\d+)\s")

# HeartRate
heartRate  = re.compile(r'HeartRate:\s*(\d+)\s*bpm')

# Bob Cadence and poweer
power = re.compile(r'SrmPower:\s*([\d\.]+)\s*W')
cadence = re.compile(r'SrmCadence:\s*([\d\.]+)\s*rpm')


pathI = '../../dati/Cerberus/balocco/20250913/rowdata'
pathO = '../../dati/Cerberus/balocco/20250913'

for nf in os.listdir(pathI):
    n,e = os.path.splitext(nf)
    if e == '.txt':
        pathFile = os.path.join(pathI, nf)
        with open(pathFile, 'r') as inF:
            dati = list()
            time = None
            dati_i = dict()
            
            for line in inF:
                timeMatch = time_pattern.search(line)
                if timeMatch:
                    time = timeMatch.group(1)
                    dati.append(dati_i)
                    dati_i = dict()
                    dati_i = {'timestamp': time}

                speed_match = speed_pattern.search(line)
                distance_match = distance_pattern.search(line)
                raw_speed_match = raw_speed_pattern.search(line)
                raw_distance_match = raw_distance_pattern.search(line)
                lat_match = lat_pattern.search(line)
                lon_match = lon_pattern.search(line)
                gear_match = gear_pattern.search(line)
                tkBattery_match = tk_battery.search(line)
                rxShiftit = rxShifting.search(line)
                heartRateM = heartRate.search(line)
                poweM = power.search(line)
                cadenceM = cadence.search(line)
                
                if speed_match:
                    dati_i['speed'] = float(speed_match.group(1))
                if distance_match:
                    dati_i['distance'] = int(distance_match.group(1))
                if raw_speed_match:
                    dati_i['raw_speed'] = float(raw_speed_match.group(1))
                if raw_distance_match:
                    dati_i['raw_distance'] = int(raw_distance_match.group(1))
                if lat_match:
                    dati_i['latitude'] = float(lat_match.group(1))
                if lon_match:
                    dati_i['longitude'] = float(lon_match.group(1))
                if gear_match:
                    dati_i['gear'] = int(gear_match.group(1))
                if tkBattery_match:
                    dati_i['tkBattery'] = float(tkBattery_match.group(1))
                if rxShiftit:
                    dati_i['rxShifting'] = int(rxShiftit.group(1))
                if heartRateM:
                    dati_i['heartRate'] = int(heartRateM.group(1))
                if cadenceM:
                    dati_i['cadence'] = float(cadenceM.group(1))
                if poweM:
                    dati_i['power'] = float(poweM.group(1))
            
            df = pd.DataFrame(dati)
            df = df.fillna(0)
            nff, _ = os.path.splitext(nf) 
            df.to_csv(os.path.join(pathO, nff + '.csv'), index=False)
        