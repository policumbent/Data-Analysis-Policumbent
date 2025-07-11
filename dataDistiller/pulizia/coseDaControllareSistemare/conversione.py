def decimali_a_dms(coord_decimale, tipo='lat'):
    """
    Converte una coordinata da formato decimale a gradi, minuti e secondi (DMS).
    
    Args:
        coord_decimale (float): La coordinata in formato decimale.
        tipo (str): 'lat' per latitudine, 'lon' per longitudine.
        
    Returns:
        str: La coordinata in formato DMS con direzione (N/S o E/W).
    """
    direzione = ''
    
    if tipo == 'lat':
        direzione = 'N' if coord_decimale >= 0 else 'S'
    elif tipo == 'lon':
        direzione = 'E' if coord_decimale >= 0 else 'W'
    
    coord_assoluta = abs(coord_decimale)
    gradi = int(coord_assoluta)
    minuti_decimali = (coord_assoluta - gradi) * 60
    minuti = int(minuti_decimali)
    secondi = (minuti_decimali - minuti) * 60

    return f"{gradi}°{minuti}'{secondi:.2f}\" {direzione}"


# Esempi di utilizzo:
lat_dec = 45.4734
lon_dec = 8.2820

lat_dms = decimali_a_dms(lat_dec, tipo='lat')
lon_dms = decimali_a_dms(lon_dec, tipo='lon')

print("Latitudine in DMS:", lat_dms)
print("Longitudine in DMS:", lon_dms)
