import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import folium


# test 2 con creazione animata del percorso

def f2(df):
    x = df['longitudine'].values
    y = df['latitudine'].values
    speed = df['velocità'].values

    img = mpimg.imread('mappa.png')

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    vmin = np.percentile(speed, 5)
    vmax = np.percentile(speed, 95)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap('plasma')
    colors = cmap(norm(speed[:-1]))  # un colore per ogni segmento

    # Imposta la figura
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_aspect('equal')
    ax.set_xlabel('Longitudine')
    ax.set_ylabel('Latitudine')
    ax.set_title('Tracciato animato con colore basato sulla velocità')

    # LineCollection iniziale (vuota)
    line = LineCollection([], linewidth=2)
    ax.add_collection(line)

    # Funzione di aggiornamento
    def update(frame):
        if frame < 2:
            line.set_segments([])  # non disegnare nulla per i primi frame
        else:
            line.set_segments(segments[:frame])
            line.set_color(colors[:frame])
        return line,

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Velocità (km/h)')


    ani = FuncAnimation(fig, update, frames=len(segments), interval=30, blit=True)
    plt.show()


# test 3 creazione mappa

def f3(df):
    from geopy.distance import geodesic  # Per calcolare la distanza geografica


    mappa = folium.Map(location=[df['latitudine'][0], df['longitudine'][0]], zoom_start=14)

    punto_partenza = (df['latitudine'][0], df['longitudine'][0])

    tolleranza = 5

    colore = "blue"  # Colore iniziale della linea
    previous_point = None
    linea_iniziata = False

    percorso = []


    for i, row in df.iterrows():
        current_point = (row['latitudine'], row['longitudine'])
        
        distanza = geodesic(current_point, punto_partenza).meters
        
        if distanza < tolleranza and not linea_iniziata:
            colore = "green" if colore == "blue" else "blue"
            linea_iniziata = True
        
        # Aggiungere il punto al percorso
        percorso.append(current_point)
        
        # Aggiungere la PolyLine con il colore corrente
        if previous_point is not None:
            folium.PolyLine([previous_point, current_point], color=colore, weight=2.5, opacity=1).add_to(mappa)
        
        # Aggiornare il punto precedente
        previous_point = current_point

    # Salvare la mappa in un file HTML
    mappa.save("percorso_bici_colori_cambiati.html")


# suddivisione giri 

def f4(df):
    print(f"long max: {df['longitudine'].max()}, long min: {df['longitudine'].min()}, lat max: {df['latitudine'].max()}, lat min: {df['latitudine'].min()}")
    df['longitudine_normalizzata'] = (df['longitudine'] - df['longitudine'].min()) / (df['longitudine'].max() - df['longitudine'].min())
    df['latitudine_normalizzata'] = (df['latitudine'] - df['latitudine'].min()) / (df['latitudine'].max() - df['latitudine'].min())

    start_long = df['longitudine_normalizzata'].iloc[0]
    start_lat = df['latitudine_normalizzata'].iloc[0]
    var = (0.9, 1.1)

    # Filtro booleano
    filtro = (
    (df['longitudine_normalizzata'] >= start_long * var[0]) &
    (df['longitudine_normalizzata'] <= start_long * var[1]) &
    (df['latitudine_normalizzata'] >= start_lat * var[0]) &
    (df['latitudine_normalizzata'] <= start_lat * var[1]))

    print("Risultati filtro:", filtro.value_counts())

    print(df[filtro][['longitudine','latitudine','tempo']])

    '''giocando con i parametri di var è possibili ottenere il momento nel quale completa un singolo giro'''



def f5(df):
    inizio = 3275.009444
    fine = 3703.93535

    filtro = (df['tempo'] >= inizio) & (df['tempo'] <= fine)
    sotto_df = df[filtro]

    #print(sotto_df)

    plt.figure(figsize=(10, 8))
    sc = plt.scatter(sotto_df['longitudine'], sotto_df['latitudine'], c=sotto_df['velocità'], cmap='viridis', s=10)
    plt.colorbar(sc, label='Velocità (km/h)')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Tracciato geografico colorato per velocità')
    plt.grid(True)
    plt.axis('equal')
    plt.show()


def main():
    fn = {
        '2': f2,
        '3': f3,
        '4': f4,
        '5': f5
    }

    df = pd.read_csv('giro2.csv')

    inpUt = input("inserisci numero funzione da chiamare: ")
    fnz = fn.get(inpUt.strip())
    if fnz:
        fnz(df)


main()