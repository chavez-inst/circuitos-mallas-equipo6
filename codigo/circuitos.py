# datos de los dos circuitos del examen tipo A
# cada rama lleva el nodo del que sale, el nodo al que entra, su impedancia, Vsk, Jsk
# y los elementos que tiene
import numpy as np


def inductor(w, henrys):
    return 1j * w * henrys


def capacitor(w, farads):
    return 1 / (1j * w * farads)


def fasor(amplitud, faseGrados):
    # una fuente A cos(wt + fase) se vuelve el fasor pico A con ese angulo
    return amplitud * np.exp(1j * np.radians(faseGrados))


# ===== 1. CIRCUITO 1 =====
# valores del examen en unidades basicas: ohms, henrys, farads, volts, amperes, grados y hertz
# la fuente de voltaje es 4 cos(10t) y la de corriente 3 cos(10t), y w = 10 son 1.59155 Hz
valoresExamen1 = {
    "R1": 1, "R2": 3, "R3": 1000,
    "L1": 0.3, "L2": 0.3,
    "C1": 0.05, "C2": 0.05, "C3": 0.05,
    "V1": 4, "faseV1": 0,
    "I1": 3, "faseI1": 0,
    "f": 10 / (2 * np.pi),
}

# cada renglon es una malla y cada columna una rama
# 1 si la rama va en el mismo sentido que la malla y -1 si va al reves
matrizMallas1 = [
    [-1, 1, 0, -1, 0, 0, 0],
    [0, -1, -1, 0, -1, 0, 0],
    [0, 0, 0, 1, 0, -1, 0],
    [0, 0, 0, 0, 1, 0, -1],
]


def armarCircuito1(valores):
    w = 2 * np.pi * valores["f"]
    fuenteVoltaje = fasor(valores["V1"], valores["faseV1"])
    fuenteCorriente = fasor(valores["I1"], valores["faseI1"])
    ramas = [
        (1, 2, valores["R1"], fuenteVoltaje, 0, "R1 y V1"),
        (1, 3, inductor(w, valores["L2"]), 0, 0, "L2"),
        (4, 1, capacitor(w, valores["C3"]), 0, fuenteCorriente, "C3 e I1"),
        (2, 3, capacitor(w, valores["C1"]), 0, 0, "C1"),
        (3, 4, valores["R2"], 0, 0, "R2"),
        (2, 3, valores["R3"] + inductor(w, valores["L1"]), 0, 0, "R3 y L1"),
        (3, 4, capacitor(w, valores["C2"]), 0, 0, "C2"),
    ]
    return {
        "nombre": "Circuito 1",
        "archivoGrafo": "reporte/img/grafo_circuito1.png",
        "w": w,
        "ramas": ramas,
        "matrizMallas": matrizMallas1,
        "nodoReferencia": 4,
        # datos solo para el dibujo del grafo
        "posiciones": {1: (2, 3), 2: (0, 1.5), 3: (2, 0), 4: (4, 1.5)},
        "curvaturas": [0, 0, 0, 0, 0, -0.5, -0.5],
        "mallas": [(1.0, 1.5, 0.35), (3.0, 1.5, 0.35), (0.75, 0.55, 0.22), (3.25, 0.55, 0.22)],
        "tierra": (1, 0),
    }


# ===== 2. CIRCUITO 2 =====
# la fuente de voltaje es 2 cos(100t) y la de corriente 5 cos(100t + 75), y w = 100 son 15.9155 Hz
valoresExamen2 = {
    "R4": 1, "R5": 1,
    "L4": 0.02, "L5": 0.02,
    "C4": 0.01,
    "V2": 2, "faseV2": 0,
    "I2": 5, "faseI2": 75,
    "f": 100 / (2 * np.pi),
}

matrizMallas2 = [
    [-1, 1, 0, 0],
    [0, -1, 1, 1],
]


def armarCircuito2(valores):
    w = 2 * np.pi * valores["f"]
    fuenteVoltaje = fasor(valores["V2"], valores["faseV2"])
    fuenteCorriente = fasor(valores["I2"], valores["faseI2"])
    ramas = [
        (1, 3, valores["R5"] + inductor(w, valores["L5"]), fuenteVoltaje, 0, "R5, L5 y V2"),
        (1, 3, capacitor(w, valores["C4"]), 0, 0, "C4"),
        (1, 2, inductor(w, valores["L4"]), 0, 0, "L4"),
        (2, 3, valores["R4"], 0, fuenteCorriente, "R4 e I2"),
    ]
    return {
        "nombre": "Circuito 2",
        "archivoGrafo": "reporte/img/grafo_circuito2.png",
        "w": w,
        "ramas": ramas,
        "matrizMallas": matrizMallas2,
        "nodoReferencia": 3,
        "posiciones": {1: (0, 2), 2: (3, 2), 3: (1.5, 0)},
        "curvaturas": [-0.4, 0, 0, 0],
        "mallas": [(0.55, 0.9, 0.16), (1.75, 1.3, 0.33)],
        "tierra": (0, -1),
    }


circuitos = [armarCircuito1(valoresExamen1), armarCircuito2(valoresExamen2)]
