# resuelve por mallas los dos circuitos del examen tipo A
# se corre desde la raiz del repositorio con: python codigo/mallas.py
import numpy as np

from circuitos import circuitos
from grafo import dibujarGrafo

np.set_printoptions(precision=4, suppress=True, linewidth=160)


def imprimirMatriz(titulo, matriz):
    print(f"\n{titulo}")
    for renglon in np.atleast_2d(matriz):
        print("   " + "   ".join(f"{z.real:10.4f}{z.imag:+10.4f}j" for z in renglon))


def imprimirPolar(titulo, vector):
    print(f"\n{titulo}")
    for k, z in enumerate(vector, start=1):
        modulo = np.abs(z)
        angulo = np.degrees(np.angle(z))
        print(f"   {k}:  {z.real:10.4f}{z.imag:+10.4f}j   =   {modulo:10.4f} /_ {angulo:8.2f} grados")


def revisarMallas(ramas, matrizMallas):
    # matriz de incidencia: renglon por nodo, columna por rama, 1 si la rama sale del nodo y -1 si entra
    nodos = sorted({rama[0] for rama in ramas} | {rama[1] for rama in ramas})
    A = np.zeros((len(nodos), len(ramas)))
    for k, rama in enumerate(ramas):
        A[nodos.index(rama[0]), k] = 1
        A[nodos.index(rama[1]), k] = -1

    # cada malla es un lazo, asi que sus ramas no pueden dejar corriente sobrando en ningun nodo
    M = np.array(matrizMallas, dtype=float)
    if not np.allclose(M @ A.T, 0):
        raise ValueError("la matriz de mallas no coincide con los nodos de las ramas")

    # tienen que ser b - n + 1 mallas independientes
    if M.shape[0] != len(ramas) - len(nodos) + 1 or np.linalg.matrix_rank(M) != M.shape[0]:
        raise ValueError("la matriz de mallas no tiene b - n + 1 mallas independientes")


def resolver(circuito):
    ramas = circuito["ramas"]
    revisarMallas(ramas, circuito["matrizMallas"])

    # impedancias, fuentes de voltaje y de corriente de cada rama
    impedancias = [complex(rama[2]) for rama in ramas]
    Z = np.diag(impedancias)
    Vsk = np.array([rama[3] for rama in ramas], dtype=complex)
    Jsk = np.array([rama[4] for rama in ramas], dtype=complex)
    M = np.array(circuito["matrizMallas"], dtype=complex)

    print("=" * 90)
    print(circuito["nombre"].upper())
    imprimirMatriz("Z, matriz de impedancias de rama", Z)
    imprimirPolar("Vsk, fuentes de voltaje de rama", Vsk)
    imprimirPolar("Jsk, fuentes de corriente de rama", Jsk)
    imprimirMatriz("M, matriz de mallas", M)
    imprimirMatriz("M transpuesta", M.T)

    # ecuaciones de mallas
    Zm = M @ Z @ M.T
    # si Zm casi no tiene inversa no hay solucion con esos valores, por ejemplo cuando
    # un inductor y un capacitor se cancelan justo a esa frecuencia
    if np.linalg.cond(Zm) > 1e12:
        raise ValueError("la matriz Zm no tiene inversa con estos valores")
    Esm = M @ Z @ Jsk - M @ Vsk
    Im = np.linalg.inv(Zm) @ Esm
    Jk = M.T @ Im
    Vk = Vsk + Z @ Jk - Z @ Jsk

    imprimirMatriz("Zm = M Z M^T, impedancias de malla", Zm)
    imprimirPolar("Esm = M Z Jsk - M Vsk, fuentes de malla", Esm)
    imprimirPolar("Im = Zm^-1 Esm, corrientes de malla", Im)
    imprimirPolar("Jk = M^T Im, corrientes de rama", Jk)
    imprimirPolar("Vk = Vsk + Z Jk - Z Jsk, voltajes de rama", Vk)
    return Jk, Vk


# ===== 1. PROGRAMA PRINCIPAL =====
# esta parte solo corre con python codigo/mallas.py, no cuando la interfaz usa resolver
if __name__ == "__main__":
    for circuito in circuitos:
        resolver(circuito)
        dibujarGrafo(circuito)
        print(f"\ngrafo guardado en {circuito['archivoGrafo']}")
