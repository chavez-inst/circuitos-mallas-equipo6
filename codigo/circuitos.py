# datos de los dos circuitos del examen tipo A
# cada rama lleva el nodo del que sale, el nodo al que entra, su impedancia, Vsk, Jsk
# y los elementos que tiene
import numpy as np


def inductor(w, henrys):
    return 1j * w * henrys


def capacitor(w, farads):
    return 1 / (1j * w * farads)


# ===== 1. CIRCUITO 1 =====
# la fuente de voltaje es 4 cos(10t) y la de corriente 3 cos(10t), asi que los fasores pico son 4 y 3
w1 = 10
ramas1 = [
    (1, 2, 1, 4, 0, "R1 y V1"),
    (1, 3, inductor(w1, 0.3), 0, 0, "L2"),
    (4, 1, capacitor(w1, 0.05), 0, 3, "C3 e I1"),
    (2, 3, capacitor(w1, 0.05), 0, 0, "C1"),
    (3, 4, 3, 0, 0, "R2"),
    (2, 3, 1000 + inductor(w1, 0.3), 0, 0, "R3 y L1"),
    (3, 4, capacitor(w1, 0.05), 0, 0, "C2"),
]

# cada renglon es una malla y cada columna una rama
# 1 si la rama va en el mismo sentido que la malla y -1 si va al reves
matrizMallas1 = [
    [-1, 1, 0, -1, 0, 0, 0],
    [0, -1, -1, 0, -1, 0, 0],
    [0, 0, 0, 1, 0, -1, 0],
    [0, 0, 0, 0, 1, 0, -1],
]

circuito1 = {
    "nombre": "Circuito 1",
    "archivoGrafo": "reporte/img/grafo_circuito1.png",
    "w": w1,
    "ramas": ramas1,
    "matrizMallas": matrizMallas1,
    "nodoReferencia": 4,
    # datos solo para el dibujo del grafo
    "posiciones": {1: (2, 3), 2: (0, 1.5), 3: (2, 0), 4: (4, 1.5)},
    "curvaturas": [0, 0, 0, 0, 0, -0.5, -0.5],
    "mallas": [(1.0, 1.5, 0.35), (3.0, 1.5, 0.35), (0.75, 0.55, 0.22), (3.25, 0.55, 0.22)],
    "tierra": (1, 0),
}

# ===== 2. CIRCUITO 2 =====
# la fuente de voltaje es 2 cos(100t) y la de corriente 5 cos(100t + 75), fasores pico
w2 = 100
corriente2 = 5 * np.exp(1j * np.radians(75))
ramas2 = [
    (1, 3, 1 + inductor(w2, 0.02), 2, 0, "R5, L5 y V2"),
    (1, 3, capacitor(w2, 0.01), 0, 0, "C4"),
    (1, 2, inductor(w2, 0.02), 0, 0, "L4"),
    (2, 3, 1, 0, corriente2, "R4 e I2"),
]

matrizMallas2 = [
    [-1, 1, 0, 0],
    [0, -1, 1, 1],
]

circuito2 = {
    "nombre": "Circuito 2",
    "archivoGrafo": "reporte/img/grafo_circuito2.png",
    "w": w2,
    "ramas": ramas2,
    "matrizMallas": matrizMallas2,
    "nodoReferencia": 3,
    "posiciones": {1: (0, 2), 2: (3, 2), 3: (1.5, 0)},
    "curvaturas": [-0.4, 0, 0, 0],
    "mallas": [(0.55, 0.9, 0.16), (1.75, 1.3, 0.33)],
    "tierra": (0, -1),
}

circuitos = [circuito1, circuito2]
