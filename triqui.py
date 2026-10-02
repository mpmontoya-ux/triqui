import random
import tkinter as tk

# Todas las líneas ganadoras: 3 filas, 3 columnas y 2 diagonales
LINEAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class LogicaTriqui:
    """Lógica del juego, sin ninguna dependencia de la interfaz."""

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.tablero = [""] * 9
        self.turno = random.choice(["X", "O"])  # empieza uno al azar
        self.ganador = None
        self.linea_ganadora = None
        self.terminado = False

    def jugar(self, posicion):
        """Marca la casilla para el jugador en turno. Devuelve True si fue válido."""
        if self.terminado or self.tablero[posicion] != "":
            return False
        self.tablero[posicion] = self.turno
        self._revisar_resultado()
        if not self.terminado:
            self.turno = "O" if self.turno == "X" else "X"
        return True

    def _revisar_resultado(self):
        for a, b, c in LINEAS:
            if self.tablero[a] and self.tablero[a] == self.tablero[b] == self.tablero[c]:
                self.ganador = self.tablero[a]
                self.linea_ganadora = (a, b, c)
                self.terminado = True
                return
        if all(self.tablero):  # tablero lleno sin ganador
            self.terminado = True


class InterfazTriqui(tk.Tk):
    """Ventana de Tkinter que muestra y controla el juego."""

    COLOR_X = "#1971c2"
    COLOR_O = "#e8590c"
    COLOR_VACIO = "#e8ecf8"
    COLOR_GANADOR = "#ffe066"
    COLOR_FONDO = "#f4f6fb"

    def __init__(self):
        super().__init__()
        self.title("Triqui")
        self.configure(bg=self.COLOR_FONDO)
        self.resizable(False, False)
        self._centrar_ventana(380, 520)

        self.juego = LogicaTriqui()

        self.etiqueta = tk.Label(
            self, font=("Arial", 18, "bold"), bg=self.COLOR_FONDO, fg="#1f2937"
        )
        self.etiqueta.pack(pady=(20, 10))

        # Tablero de 3x3 con botones grandes
        marco = tk.Frame(self, bg=self.COLOR_FONDO)
        marco.pack()
        self.botones = []
        for i in range(9):
            boton = tk.Button(
                marco, text="", font=("Arial", 36, "bold"), width=3, height=1,
                bg=self.COLOR_VACIO, relief="flat",
                command=lambda pos=i: self.al_hacer_clic(pos),
            )
            boton.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.botones.append(boton)

        self.boton_reiniciar = tk.Button(
            self, text="Jugar de nuevo", font=("Arial", 14, "bold"),
            command=self.reiniciar, state="disabled",
        )
        self.boton_reiniciar.pack(pady=20)

        self.actualizar()

    def _centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def al_hacer_clic(self, posicion):
        if self.juego.jugar(posicion):
            self.actualizar()

    def reiniciar(self):
        self.juego.reiniciar()
        self.actualizar()

    def _color_de(self, simbolo):
        return self.COLOR_X if simbolo == "X" else self.COLOR_O

    def actualizar(self):
        juego = self.juego

        for i, boton in enumerate(self.botones):
            simbolo = juego.tablero[i]
            boton.config(
                text=simbolo,
                fg=self._color_de(simbolo) if simbolo else "black",
                bg=self.COLOR_VACIO,
                state="disabled" if (simbolo or juego.terminado) else "normal",
                disabledforeground=self._color_de(simbolo) if simbolo else "black",
            )

        # Resalta la línea ganadora
        if juego.linea_ganadora:
            for i in juego.linea_ganadora:
                self.botones[i].config(bg=self.COLOR_GANADOR)

        if juego.ganador:
            texto = f"¡Ganó el jugador {juego.ganador}!"
            color = self._color_de(juego.ganador)
        elif juego.terminado:
            texto, color = "¡Empate!", "#1f2937"
        else:
            texto = f"Turno del jugador {juego.turno}"
            color = self._color_de(juego.turno)
        self.etiqueta.config(text=texto, fg=color)

        # El botón de reiniciar solo se habilita al terminar la partida
        self.boton_reiniciar.config(state="normal" if juego.terminado else "disabled")


if __name__ == "__main__":
    InterfazTriqui().mainloop()
