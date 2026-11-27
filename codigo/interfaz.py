# interfaz grafica: muestra la portada del equipo y luego cada circuito con casillas
# para cambiar sus valores, y lo resuelve por mallas con la misma funcion del programa
# se corre desde la raiz del repositorio con: python codigo/interfaz.py
import contextlib
import ctypes
import io
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from circuitos import armarCircuito1, armarCircuito2, valoresExamen1, valoresExamen2
from grafo import figuraGrafo
from mallas import resolver

# los textos con acentos van con su codigo unicode para que el archivo siga siendo ascii
OHM = "\u03a9"
MICRO = "\u00b5"
GRADOS = "\u00b0"
ANGULO = "\u2220"

INTEGRANTES = [
    "Ch\u00e1vez L\u00f3pez Brayan Alejandro",
    "Daniel Kaleb Villanueva Figueroa",
    "Enrique Hernandez Chanelo",
    "Israel Raymundo V\u00e1zquez",
    "Ortega Novoa Octavio",
]

# cada unidad con el numero por el que se multiplica para pasarla a ohms, henrys o farads
UNIDADES = {
    "R": {OHM: 1, "k" + OHM: 1e3},
    "L": {"H": 1, "mH": 1e-3},
    "C": {"F": 1, "mF": 1e-3, MICRO + "F": 1e-6},
}


# ===== 1. DATOS DE CADA PANTALLA =====
# las posiciones estan en pixeles de la imagen original del circuito
# tapar son los rectangulos blancos que borran los valores impresos en el dibujo
# cada componente lleva su nombre, donde va su casilla y la unidad con la que empieza
# cada fuente lleva su nombre, donde van sus casillas, la unidad de su amplitud
# y si ahi va la casilla de la frecuencia
PANTALLA1 = {
    "titulo": "Circuito 1",
    "imagen": "reporte/img/circuito1.png",
    "anchoImagen": 640,
    "armar": armarCircuito1,
    "valoresExamen": valoresExamen1,
    "tapar": [
        (385, 100, 447, 134), (680, 306, 762, 347), (1074, 276, 1174, 317), (1354, 286, 1414, 327),
        (110, 328, 294, 460), (312, 630, 414, 674), (792, 608, 854, 648), (86, 796, 160, 838),
        (270, 942, 360, 984), (986, 962, 1094, 1004), (1400, 985, 1430, 1010),
    ],
    "textos": [],
    "componentes": [
        ("R1", 387, 117, OHM), ("L2", 682, 326, "H"), ("C3", 1076, 296, "F"),
        ("C1", 314, 652, "F"), ("R2", 794, 628, OHM), ("R3", 88, 817, "k" + OHM),
        ("L1", 272, 963, "H"), ("C2", 988, 983, "F"),
    ],
    "fuentes": [("V1", 112, 330, "V pico", True), ("I1", 1356, 288, "A pico", False)],
}

PANTALLA2 = {
    "titulo": "Circuito 2",
    "imagen": "reporte/img/circuito2.png",
    "anchoImagen": 660,
    "armar": armarCircuito2,
    "valoresExamen": valoresExamen2,
    "tapar": [
        (355, 95, 467, 137), (880, 90, 997, 132), (90, 193, 148, 237), (1197, 265, 1257, 312),
        (632, 385, 730, 432), (120, 410, 347, 562), (1435, 262, 1492, 302), (1195, 220, 1257, 262),
    ],
    # la casilla de R4 no cabe entre R4 e I2, asi que va a la izquierda junto con su nombre
    "textos": [("R4", 1150, 240)],
    "componentes": [
        ("L5", 357, 116, "mH"), ("L4", 882, 111, "mH"), ("R5", 90, 215, OHM),
        ("R4", 935, 287, OHM), ("C4", 634, 409, "mF"),
    ],
    "fuentes": [("V2", 122, 420, "V pico", True), ("I2", 1437, 262, "A pico", False)],
}


# las medidas en pixeles se multiplican por esta escala para que en pantallas con
# zoom de windows las imagenes crezcan igual que las letras
escalaPantalla = 1


def px(medida):
    return round(medida * escalaPantalla)


def rutaArchivo(ruta):
    # el ejecutable guarda las imagenes en una carpeta temporal, y con python
    # se toman desde la raiz del repositorio
    if hasattr(sys, "_MEIPASS"):
        raiz = sys._MEIPASS
    else:
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(raiz, ruta)


def cargarImagen(ruta, ancho=None, alto=None):
    imagen = Image.open(rutaArchivo(ruta))
    if ancho is not None:
        alto = round(imagen.height * ancho / imagen.width)
    else:
        ancho = round(imagen.width * alto / imagen.height)
    return ImageTk.PhotoImage(imagen.resize((ancho, alto), Image.LANCZOS))


def textoPolar(z):
    return f"{np.abs(z):.4f} {ANGULO} {np.degrees(np.angle(z)):.2f}{GRADOS}"


# ===== 2. PORTADA =====
def crearPortada(ventana, abrirCircuito):
    portada = ttk.Frame(ventana, padding=20)
    ventana.logos = [cargarImagen("reporte/logos/Logo_UNAM.png", alto=px(150)),
                     cargarImagen("reporte/logos/Logo_FI.png", alto=px(150))]

    encabezado = ttk.Frame(portada)
    encabezado.pack(fill="x")
    ttk.Label(encabezado, image=ventana.logos[0]).pack(side="left")
    ttk.Label(encabezado, image=ventana.logos[1]).pack(side="right")
    titulos = ttk.Frame(encabezado)
    titulos.pack(expand=True)
    ttk.Label(titulos, text="FACULTAD DE INGENIER\u00cdA, UNAM", font=("Segoe UI", 16, "bold")).pack(pady=(20, 8))
    ttk.Label(titulos, text="CIRCUITOS EL\u00c9CTRICOS", font=("Segoe UI", 13, "bold")).pack(pady=4)
    ttk.Label(titulos, text="M\u00c9TODOS SISTEM\u00c1TICOS DE AN\u00c1LISIS\nDE CIRCUITOS EL\u00c9CTRICOS",
              font=("Segoe UI", 13, "bold"), justify="center").pack(pady=4)
    ttk.Label(titulos, text="EXAMEN TIPO A", font=("Segoe UI", 11, "bold")).pack(pady=4)

    datos = ttk.Frame(portada)
    datos.pack(pady=20)
    renglones = [("Equipo:", "6"), ("Tipo de examen:", "A"), ("Integrantes:", "\n".join(INTEGRANTES)),
                 ("Semestre:", "2027-1")]
    for k, (etiqueta, valor) in enumerate(renglones):
        ttk.Label(datos, text=etiqueta, font=("Segoe UI", 10, "bold")).grid(row=k, column=0, sticky="ne", padx=6, pady=2)
        ttk.Label(datos, text=valor, font=("Segoe UI", 10)).grid(row=k, column=1, sticky="nw", pady=2)

    ttk.Label(portada, text="Elige el circuito que quieres resolver por mallas:", font=("Segoe UI", 10)).pack(pady=(10, 6))
    botones = ttk.Frame(portada)
    botones.pack()
    ttk.Button(botones, text="Circuito 1", command=lambda: abrirCircuito(0)).pack(side="left", padx=10, ipadx=10, ipady=4)
    ttk.Button(botones, text="Circuito 2", command=lambda: abrirCircuito(1)).pack(side="left", padx=10, ipadx=10, ipady=4)
    return portada


# ===== 3. PANTALLA DE UN CIRCUITO =====
class PantallaCircuito(ttk.Frame):
    def __init__(self, ventana, datos, irAPortada):
        super().__init__(ventana, padding=8)
        self.datos = datos
        # para cada valor se guarda su casilla y, si tiene, la lista de unidades
        self.casillas = {}
        self.unidades = {}

        arriba = ttk.Frame(self)
        arriba.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        ttk.Button(arriba, text="< Portada", command=irAPortada).pack(side="left")
        ttk.Label(arriba, text=f"{datos['titulo']}: resolver por mallas",
                  font=("Segoe UI", 13, "bold")).pack(side="left", padx=12)

        self.crearDibujo()

        botones = ttk.Frame(self)
        botones.grid(row=2, column=0, sticky="w", pady=6)
        ttk.Button(botones, text="Resolver", command=self.resolverCircuito).pack(side="left", ipadx=8)
        ttk.Button(botones, text="Valores del examen", command=self.ponerValoresExamen).pack(side="left", padx=8)
        ttk.Button(botones, text="Ver grafo", command=self.verGrafo).pack(side="left")
        ttk.Label(self, text="Las fuentes son A cos(2\u03c0ft + fase) y las dos usan la misma frecuencia. "
                  "Los resultados son fasores pico.", foreground="#444").grid(row=3, column=0, sticky="w")

        self.crearResultados()
        self.ponerValoresExamen()

    # ---------- dibujo del circuito con sus casillas ----------
    def crearDibujo(self):
        ancho = px(self.datos["anchoImagen"])
        self.imagen = cargarImagen(self.datos["imagen"], ancho=ancho)
        escala = ancho / Image.open(rutaArchivo(self.datos["imagen"])).width
        # el lienzo es mas ancho que la imagen para que quepan las casillas de la fuente de corriente
        lienzo = tk.Canvas(self, width=ancho + px(110), height=self.imagen.height(), bg="white", highlightthickness=0)
        lienzo.grid(row=1, column=0, sticky="nw")
        lienzo.create_image(0, 0, image=self.imagen, anchor="nw")

        for x1, y1, x2, y2 in self.datos["tapar"]:
            lienzo.create_rectangle(x1 * escala, y1 * escala, x2 * escala, y2 * escala, fill="white", outline="")

        for texto, x, y in self.datos["textos"]:
            lienzo.create_text(x * escala, y * escala, text=texto, font=("Arial", 12, "bold"), anchor="e")

        for nombre, x, y, unidad in self.datos["componentes"]:
            marco = tk.Frame(lienzo, bg="white")
            casilla = ttk.Entry(marco, width=6)
            casilla.pack(side="left")
            opciones = list(UNIDADES[nombre[0]].keys())
            lista = ttk.Combobox(marco, values=opciones, width=3, state="readonly")
            lista.pack(side="left")
            self.casillas[nombre] = casilla
            self.unidades[nombre] = lista
            lienzo.create_window(x * escala, y * escala, window=marco, anchor="w")

        for nombre, x, y, unidadAmplitud, llevaFrecuencia in self.datos["fuentes"]:
            marco = tk.Frame(lienzo, bg="white")
            renglones = [(nombre, unidadAmplitud), ("fase" + nombre, "grados")]
            if llevaFrecuencia:
                renglones.append(("f", "Hz"))
            for k, (clave, texto) in enumerate(renglones):
                casilla = ttk.Entry(marco, width=8)
                casilla.grid(row=k, column=0, pady=1)
                tk.Label(marco, text=texto, bg="white").grid(row=k, column=1, sticky="w", padx=2)
                self.casillas[clave] = casilla
            lienzo.create_window(x * escala, y * escala, window=marco, anchor="nw")

    # ---------- tabla de resultados y procedimiento ----------
    def crearResultados(self):
        pestanas = ttk.Notebook(self, width=px(470))
        pestanas.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=(10, 0))

        hojaResultados = ttk.Frame(pestanas, padding=6)
        pestanas.add(hojaResultados, text="Resultados")
        self.aviso = ttk.Label(hojaResultados, text="Escribe los valores y presiona Resolver.")
        self.aviso.pack(anchor="w", pady=(0, 6))
        columnas = ("rama", "elementos", "corriente", "voltaje")
        self.tabla = ttk.Treeview(hojaResultados, columns=columnas, show="headings", height=8)
        encabezados = ["Rama", "Elementos", "Jk (A)", "Vk (V)"]
        anchos = [50, 100, 150, 150]
        for columna, encabezado, anchoColumna in zip(columnas, encabezados, anchos):
            self.tabla.heading(columna, text=encabezado)
            self.tabla.column(columna, width=px(anchoColumna), anchor="center")
        self.tabla.pack(fill="both", expand=True)

        hojaProcedimiento = ttk.Frame(pestanas, padding=6)
        pestanas.add(hojaProcedimiento, text="Procedimiento")
        self.procedimiento = tk.Text(hojaProcedimiento, wrap="none", font=("Consolas", 9), height=20)
        barraVertical = ttk.Scrollbar(hojaProcedimiento, orient="vertical", command=self.procedimiento.yview)
        barraHorizontal = ttk.Scrollbar(hojaProcedimiento, orient="horizontal", command=self.procedimiento.xview)
        self.procedimiento.configure(yscrollcommand=barraVertical.set, xscrollcommand=barraHorizontal.set)
        self.procedimiento.grid(row=0, column=0, sticky="nsew")
        barraVertical.grid(row=0, column=1, sticky="ns")
        barraHorizontal.grid(row=1, column=0, sticky="ew")
        hojaProcedimiento.rowconfigure(0, weight=1)
        hojaProcedimiento.columnconfigure(0, weight=1)

    # ---------- valores ----------
    def ponerValoresExamen(self):
        valores = self.datos["valoresExamen"]
        for nombre, x, y, unidad in self.datos["componentes"]:
            factor = UNIDADES[nombre[0]][unidad]
            self.escribir(nombre, f"{valores[nombre] / factor:g}")
            self.unidades[nombre].set(unidad)
        for nombre, x, y, unidadAmplitud, llevaFrecuencia in self.datos["fuentes"]:
            self.escribir(nombre, f"{valores[nombre]:g}")
            self.escribir("fase" + nombre, f"{valores['fase' + nombre]:g}")
        self.escribir("f", f"{valores['f']:.8g}")

    def escribir(self, clave, texto):
        self.casillas[clave].delete(0, "end")
        self.casillas[clave].insert(0, texto)

    def leerValores(self):
        # regresa los valores en ohms, henrys, farads, volts, amperes, grados y hertz
        # o lanza ValueError con el mensaje para el usuario
        valores = {}
        for clave, casilla in self.casillas.items():
            try:
                numero = float(casilla.get())
            except ValueError:
                numero = float("nan")
            if not np.isfinite(numero):
                raise ValueError(f"Falta el valor de {clave} o no se entiende. "
                                 "Usa punto decimal, por ejemplo 0.05.")
            # las fases si pueden ser negativas
            if numero < 0 and not clave.startswith("fase"):
                raise ValueError(f"{clave} no puede ser negativo.")
            if numero == 0 and clave.startswith("C"):
                raise ValueError(f"{clave} no puede valer cero, porque un capacitor de 0 F "
                                 "tendr\u00eda impedancia infinita.")
            if numero == 0 and clave == "f":
                raise ValueError("La frecuencia tiene que ser mayor que cero.")
            if clave in self.unidades:
                numero = numero * UNIDADES[clave[0]][self.unidades[clave].get()]
            valores[clave] = numero
        return valores

    # ---------- resolver ----------
    def resolverCircuito(self):
        try:
            valores = self.leerValores()
            circuito = self.datos["armar"](valores)
            # lo que imprime resolver se guarda para mostrarlo en la pestana de procedimiento
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                Jk, Vk = resolver(circuito)
        except ValueError as error:
            mensaje = str(error)
            if "Zm" in mensaje:
                mensaje = ("Con estos valores la matriz Zm no tiene inversa, por ejemplo porque "
                           "un inductor y un capacitor se cancelan a esa frecuencia.")
            messagebox.showwarning("Revisa los valores", mensaje + "\n\nCambia los valores e intenta de nuevo.")
            return

        self.tabla.delete(*self.tabla.get_children())
        for k, rama in enumerate(circuito["ramas"]):
            self.tabla.insert("", "end", values=(f"b{k + 1}", rama[5], textoPolar(Jk[k]), textoPolar(Vk[k])))
        self.aviso.configure(text="Fasores pico de cada rama. El procedimiento completo est\u00e1 en la otra pesta\u00f1a.")

        self.procedimiento.configure(state="normal")
        self.procedimiento.delete("1.0", "end")
        self.procedimiento.insert("1.0", salida.getvalue())
        self.procedimiento.configure(state="disabled")

    def verGrafo(self):
        # el grafo no depende de los valores, asi que se dibuja con los del examen
        circuito = self.datos["armar"](self.datos["valoresExamen"])
        ventanaGrafo = tk.Toplevel(self)
        ventanaGrafo.title(f"Grafo orientado del {self.datos['titulo'].lower()}")
        figura = figuraGrafo(circuito)
        dibujo = FigureCanvasTkAgg(figura, master=ventanaGrafo)
        dibujo.draw()
        dibujo.get_tk_widget().pack(fill="both", expand=True)


# ===== 4. PROGRAMA PRINCIPAL =====
def main():
    global escalaPantalla
    # asi windows no estira la ventana borrosa, y la escala se calcula aqui para cualquier zoom
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass
    ventana = tk.Tk()
    escalaPantalla = ventana.winfo_fpixels("1i") / 96
    ventana.title("M\u00e9todos sistem\u00e1ticos de an\u00e1lisis: equipo 6, examen A")
    ventana.configure(bg="white")
    estilo = ttk.Style()
    estilo.configure("TFrame", background="white")
    estilo.configure("TLabel", background="white")
    estilo.configure("Treeview", rowheight=px(22))

    pantallas = []

    def mostrar(pantalla):
        for otra in [portada] + pantallas:
            otra.pack_forget()
        pantalla.pack(fill="both", expand=True)

    portada = crearPortada(ventana, lambda numero: mostrar(pantallas[numero]))
    for datos in [PANTALLA1, PANTALLA2]:
        pantallas.append(PantallaCircuito(ventana, datos, lambda: mostrar(portada)))

    mostrar(portada)
    ventana.mainloop()


if __name__ == "__main__":
    main()
