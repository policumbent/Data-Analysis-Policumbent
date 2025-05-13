import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


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

'''df = df.sort_values(by='tempo').reset_index(drop=True)

# Setup figura
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(df['longitudine'].min(), df['longitudine'].max())
ax.set_ylim(df['latitudine'].min(), df['latitudine'].max())
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

plt.show()'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import matplotlib.image as mpimg


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


