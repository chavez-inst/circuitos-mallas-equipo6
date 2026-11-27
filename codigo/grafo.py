# dibuja el grafo orientado de un circuito como en el pizarron
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RADIO_NODO = 0.2


def puntoMedio(inicio, fin, curvatura):
    # punto de control de una curva cuadratica a un lado de la recta que une los nodos
    inicio = np.array(inicio, dtype=float)
    fin = np.array(fin, dtype=float)
    direccion = fin - inicio
    izquierda = np.array([-direccion[1], direccion[0]])
    control = (inicio + fin) / 2 + curvatura * izquierda
    return inicio, control, fin


def dibujarRama(ax, inicio, fin, curvatura, nombre):
    p0, p1, p2 = puntoMedio(inicio, fin, curvatura)
    t = np.linspace(0, 1, 60)[:, None]
    curva = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
    ax.plot(curva[:, 0], curva[:, 1], color="black", lw=1.6, zorder=1)

    # la flecha va en la mitad de la rama y apunta al nodo al que entra
    medio = 0.25 * p0 + 0.5 * p1 + 0.25 * p2
    tangente = (p2 - p0) / np.linalg.norm(p2 - p0)
    ax.annotate("", xy=medio + 0.05 * tangente, xytext=medio - 0.05 * tangente,
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6, mutation_scale=20),
                zorder=3)

    # el nombre de la rama va del lado al que se curva, y a la izquierda si es recta
    normal = np.array([-tangente[1], tangente[0]])
    if curvatura < 0:
        normal = -normal
    ax.text(*(medio + 0.28 * normal), nombre, color="tab:blue", fontsize=12,
            ha="center", va="center", zorder=4)


def dibujarMalla(ax, centro, radio, nombre):
    # flecha circular en el sentido de las manecillas del reloj
    x, y = centro
    angulos = np.radians(np.linspace(110, 110 - 290, 60))
    ax.plot(x + radio * np.cos(angulos), y + radio * np.sin(angulos), color="tab:red", lw=1.3, zorder=2)
    punta = np.array([x + radio * np.cos(angulos[-1]), y + radio * np.sin(angulos[-1])])
    antes = np.array([x + radio * np.cos(angulos[-4]), y + radio * np.sin(angulos[-4])])
    ax.annotate("", xy=punta, xytext=antes,
                arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.3, mutation_scale=14), zorder=3)
    ax.text(x, y, nombre, color="tab:red", fontsize=10, ha="center", va="center", zorder=4)


def dibujarTierra(ax, posicion, direccion):
    # simbolo de tierra pegado al nodo de referencia
    direccion = np.array(direccion, dtype=float)
    perpendicular = np.array([-direccion[1], direccion[0]])
    base = np.array(posicion, dtype=float) + direccion * RADIO_NODO
    extremo = base + direccion * 0.3
    ax.plot(*zip(base, extremo), color="black", lw=1.6)
    for k, mitad in enumerate([0.22, 0.14, 0.06]):
        centro = extremo + direccion * 0.1 * k
        a = centro + perpendicular * mitad
        b = centro - perpendicular * mitad
        ax.plot(*zip(a, b), color="black", lw=1.6)


def figuraGrafo(circuito):
    posiciones = circuito["posiciones"]
    fig, ax = plt.subplots(figsize=(7, 5))

    for k, rama in enumerate(circuito["ramas"]):
        inicio = posiciones[rama[0]]
        fin = posiciones[rama[1]]
        dibujarRama(ax, inicio, fin, circuito["curvaturas"][k], f"b{k + 1}")

    for k, (x, y, radio) in enumerate(circuito["mallas"]):
        dibujarMalla(ax, (x, y), radio, f"M{k + 1}")

    for nodo, (x, y) in posiciones.items():
        ax.add_patch(plt.Circle((x, y), RADIO_NODO, facecolor="white", edgecolor="black", lw=1.6, zorder=5))
        ax.text(x, y, str(nodo), fontsize=13, ha="center", va="center", zorder=6)

    dibujarTierra(ax, posiciones[circuito["nodoReferencia"]], circuito["tierra"])

    ax.set_aspect("equal")
    ax.axis("off")
    ax.margins(0.12)
    return fig


def dibujarGrafo(circuito):
    fig = figuraGrafo(circuito)
    # la ruta del archivo se toma desde la raiz del repositorio, se corra desde donde se corra
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo = os.path.join(raiz, circuito["archivoGrafo"])
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    fig.savefig(archivo, dpi=200, bbox_inches="tight")
    plt.close(fig)
