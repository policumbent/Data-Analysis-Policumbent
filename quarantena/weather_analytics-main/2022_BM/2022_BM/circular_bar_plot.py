import numpy as np
import matplotlib.pyplot as plt

dati = [1, 3, 300, 350]
def istogramma_circolare(dati):
    N = 80

    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    radii = dati
    width = (2*np.pi) / N

    ax = plt.subplot(111, polar=True)
    bars = ax.bar(theta, radii, width=width)

    # Use custom colors and opacity
    #for r, bar in zip(radii, bars):
    #    bar.set_facecolor(plt.cm.jet(r / 10.))
    #    bar.set_alpha(0.8)

    plt.show()

istogramma_circolare(dati)