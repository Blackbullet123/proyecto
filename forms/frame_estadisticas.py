from customtkinter import *
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from forms.imprimir_funcion import imprimir_grafica


class FrameEstadisticas(CTkFrame):
    def __init__(self, parent,controlador):
        super().__init__(parent, fg_color=("#EEEEEE", "#1A1A1A"))

        self.controlador=controlador

        ctk.set_default_color_theme("green")

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="control_alquiler_Reych",
            autocommit=True
        )

        self.datos_actuales = None
        self.canvas = None

        frame_superior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))

        frame_superior.pack(fill=X, pady=10)


        titulo = CTkLabel(frame_superior,text="ESTADÍSTICAS",text_color=("#00501B", "#00FF7F"),font=("Impact", 45))

        titulo.pack(side=RIGHT, padx=60)

        img = Image.open("imagenes/imprimir.png")
        img_white = Image.open("imagenes/imprimir_white.png")
        imprimir_icon = CTkImage(light_image=img, dark_image=img_white, size=(40,40))

        imprimir = CTkButton(frame_superior, hover_color=("#EEEEEE", "#2D2D2D"), command=imprimir_grafica,cursor="hand2" ,image=imprimir_icon , text="", fg_color="transparent",

                               width=30, height=30)
        imprimir.pack(side=RIGHT,padx=3)


        self.frame_grafico = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))

        self.frame_grafico.pack(expand=True, fill=BOTH, padx=30, pady=20)

        self.actualizar_en_tiempo_real()

    def consultar_datos(self):
        cursor = self.mydb.cursor()
        cursor.execute("""
            SELECT m.Nombre, COUNT(a.COD_Alquiler)
            FROM alquiler a
            INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa
            INNER JOIN marca m ON v.ID_Marca = m.ID
            GROUP BY m.Nombre
            ORDER BY COUNT(a.COD_Alquiler) DESC
        """)
        datos = cursor.fetchall()
        cursor.close()
        return datos

    def actualizar_en_tiempo_real(self):
        nuevos_datos = self.consultar_datos()
        modo_actual = get_appearance_mode()
        
        # Inicializamos ultimo_modo si no existe
        if not hasattr(self, 'ultimo_modo'):
            self.ultimo_modo = modo_actual

        # Redibujar si los datos cambiaron O si el modo de apariencia cambió
        if nuevos_datos != self.datos_actuales or modo_actual != self.ultimo_modo:
            self.datos_actuales = nuevos_datos
            self.ultimo_modo = modo_actual
            self.redibujar_grafico(nuevos_datos)

        self.after(3000, self.actualizar_en_tiempo_real)

    def actualizar_ahora(self):
        """Fuerza un redibujado inmediato del gráfico"""
        nuevos_datos = self.consultar_datos()
        self.datos_actuales = nuevos_datos
        self.ultimo_modo = get_appearance_mode()
        self.redibujar_grafico(nuevos_datos)

    def redibujar_grafico(self, datos):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        if not datos:
            CTkLabel(self.frame_grafico, text="No hay datos", font=("Arial", 16), text_color="gray").pack(pady=30)
            return

        marcas = [d[0] for d in datos]
        cantidades = [d[1] for d in datos]

        is_light = get_appearance_mode() == "Light"
        text_color = "black" if is_light else "white"
        bg_color = "#EEEEEE" if is_light else "#1A1A1A"
        bar_color = "#00501B" if is_light else "#00FF7F"

        fig = Figure(figsize=(8, 4.5), dpi=90)
        fig.patch.set_facecolor(bg_color)
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        ax.bar(marcas, cantidades, color=bar_color)
        ax.set_xlabel("Marca", color=text_color)
        ax.set_ylabel("Total", color=text_color)
        ax.tick_params(colors=text_color)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Color de los bordes del gráfico
        for spine in ax.spines.values():
            spine.set_color(text_color)

        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg=bg_color, highlightthickness=0)
        canvas_widget.pack(expand=True, fill=BOTH)

    def destroy(self):
        if self.mydb.is_connected():
            self.mydb.close()
        super().destroy()
