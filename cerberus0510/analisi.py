import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import folium


df = pd.read_csv('giro1.csv')


# test 1 tutti i dati buttati iniseme 

'''plt.figure(figsize=(10, 8))
sc = plt.scatter(df['longitudine'], df['latitudine'], c=df['velocità'], cmap='viridis', s=10)
plt.colorbar(sc, label='Velocità (km/h)')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.title('Tracciato geografico colorato per velocità')
plt.grid(True)
plt.axis('equal')
plt.show()'''


# test 2 con creazione animata del percorso

'''
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
plt.show()'''


# test 3 creazione mappa

mappa = folium.Map(location=[df['latitudine'][0], df['longitudine'][0]], zoom_start=14)

percorso = list(zip(df['latitudine'], df['longitudine']))
folium.PolyLine(locations=percorso, color="blue", weight=2.5, opacity=1).add_to(mappa)

mappa.save("percorso_bici.html")

