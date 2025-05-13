import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


df = pd.read_csv('giro1.csv')

'''plt.figure(figsize=(10, 8))
sc = plt.scatter(df['longitudine'], df['latitudine'], c=df['velocità'], cmap='viridis', s=10)
plt.colorbar(sc, label='Velocità (km/h)')
plt.xlabel('Longitudine')
plt.ylabel('Latitudine')
plt.title('Tracciato geografico colorato per velocità')
plt.grid(True)
plt.axis('equal')
plt.show()'''


df = df.sort_values(by='tempo').reset_index(drop=True)

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

plt.show()
