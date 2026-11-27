# Métodos sistemáticos de análisis de circuitos eléctricos

Proyecto del equipo 6 de Circuitos Eléctricos (FI-UNAM, 2027-1). Resolvemos los dos circuitos del examen tipo A
por el método de mallas en forma matricial, con un programa en Python que arma las matrices, calcula las corrientes
y voltajes de cada rama y dibuja el grafo de cada circuito.

El programa tiene una interfaz gráfica: muestra la portada del equipo y luego el dibujo de cada circuito con una
casilla junto a cada componente, para resolverlo con los valores del examen o con otros.

## Contenido

- `codigo/`: el programa.
  - `circuitos.py`: las ramas y la matriz de mallas de cada circuito.
  - `mallas.py`: el método de mallas.
  - `grafo.py`: el dibujo del grafo.
  - `interfaz.py`: la interfaz gráfica.
  - `crear_ejecutable.ps1`: crea el `.exe` de la interfaz.
- `reporte/`: el reporte en LaTeX.
- `img/`: la hoja del examen.

## Cómo correrlo

Con el ejecutable `Mallas_Equipo6.exe` solo hay que darle doble clic; no necesita Python. Como no está firmado,
Windows puede mostrar "Windows protegió su PC": se abre con *Más información → Ejecutar de todas formas*.

Con Python 3 se necesitan `numpy`, `matplotlib` y `pillow`:

```
pip install numpy matplotlib pillow
```

Desde la raíz del repositorio, la interfaz se abre con:

```
python codigo/interfaz.py
```

y la versión de terminal, que imprime las matrices de los dos circuitos y guarda los grafos en `reporte/img/`, con:

```
python codigo/mallas.py
```

## Cómo crear el ejecutable

Con `pip install pyinstaller` y luego, desde la raíz del repositorio:

```
powershell -ExecutionPolicy Bypass -File codigo/crear_ejecutable.ps1
```

El archivo queda en `entregables/Mallas_Equipo6.exe`.
