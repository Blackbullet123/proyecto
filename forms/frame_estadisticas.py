from customtkinter import *
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from forms.imprimir_funcion import imprimir_grafica
import matplotlib.pyplot as plt
import numpy as np

class FrameEstadisticas(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=("#EEEEEE", "#1A1A1A"))

        self.controlador = controlador
        ctk.set_default_color_theme("green")

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="control_alquiler_Reych",
            autocommit=True
        )

        # Cache para datos y estado
        self.datos_kpis = (None, None, None)
        self.datos_mensuales = None
        self.datos_marcas = None
        self.ultimo_modo = get_appearance_mode()
        self.canvas_mensual = None
        self.canvas_marcas = None
        self._after_id = None

        self.crear_interfaz()
        self.actualizar_en_tiempo_real()

    def crear_interfaz(self):
        # Frame Superior
        self.frame_superior = CTkFrame(self, fg_color="transparent", height=80)
        self.frame_superior.pack(fill=X, padx=30, pady=(20, 10))

        titulo = CTkLabel(self.frame_superior, text="ESTADÍSTICAS", 
                          text_color=("#00501B", "#00FF7F"), 
                          font=("Impact", 45))
        titulo.pack(side=RIGHT, padx=20)

        # Botón Imprimir
        try:
            img = Image.open("imagenes/imprimir.png")
            img_white = Image.open("imagenes/imprimir_white.png")
            imprimir_icon = CTkImage(light_image=img, dark_image=img_white, size=(35, 35))
            
            imprimir_btn = CTkButton(self.frame_superior, text="", 
                                     image=imprimir_icon, 
                                     fg_color="transparent", hover_color=("#EEEEEE", "#2D2D2D"),
                                     command=lambda: imprimir_grafica(self.controlador.tipo_usuario), cursor="hand2",
                                     width=40)
            imprimir_btn.pack(side=RIGHT, padx=5)
        except Exception as e:
            print(f"Error loading print icon: {e}")

        # Botón Historial
        if hasattr(self.controlador, 'mostrar_historial'):
            try:
                img_historial = Image.open("imagenes/historial.png")
                historial_icon = CTkImage(light_image=img_historial, dark_image=img_historial, size=(30, 30))
                btn_historial = CTkButton(self.frame_superior, text=" Historial",
                                         fg_color="transparent", command=self.controlador.mostrar_historial,
                                         image=historial_icon, hover_color="#00501B", 
                                         text_color=("black", "white"), font=("Ubuntu", 18, "bold"))
                btn_historial.pack(side=LEFT, padx=20)
            except Exception as e:
                print(f"Error loading history icon: {e}")

        # Area de contenido con scroll
        self.scroll_frame = CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(expand=True, fill=BOTH, padx=20, pady=10)

        # KPI Cards Frame
        self.frame_kpis = CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_kpis.pack(fill=X, pady=10)
        
        # Grid para gráficos
        self.frame_grids = CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_grids.pack(expand=True, fill=BOTH, pady=10)
        self.frame_grids.columnconfigure((0, 1), weight=1)

        # Inicializar Placeholders para KPIs
        self.kpi_labels = {}
        self.kpi_labels['total'] = self.crear_kpi_card(self.frame_kpis, "TOTAL ALQUILERES", "0", 0)
        self.kpi_labels['mes'] = self.crear_kpi_card(self.frame_kpis, "ALQUILERES ESTE MES", "0", 1)
        self.kpi_labels['marca'] = self.crear_kpi_card(self.frame_kpis, "MARCA PREFERIDA", "N/A", 2)

        # Inicializar Placeholders para Gráficos
        self.container_mensual = CTkFrame(self.frame_grids, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15)
        self.container_mensual.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.container_marcas = CTkFrame(self.frame_grids, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15)
        self.container_marcas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def crear_kpi_card(self, parent, titulo, valor_inicial, col):
        card = CTkFrame(parent, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15, 
                        border_width=1, border_color=("#E0E0E0", "#333333"))
        card.grid(row=0, column=col, padx=10, sticky="ew")
        parent.columnconfigure(col, weight=1)
        
        CTkLabel(card, text=titulo, font=("Ubuntu", 14), text_color="gray").pack(pady=(15, 0))
        label_valor = CTkLabel(card, text=valor_inicial, font=("Ubuntu", 28, "bold"), text_color=("#00501B", "#00FF7F"))
        label_valor.pack(pady=(5, 15))
        return label_valor

    def consultar_data(self):
        try:
            cursor = self.mydb.cursor()
            
            # Consultar KPIs
            cursor.execute("SELECT COUNT(*) FROM alquiler")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM alquiler WHERE MONTH(Fecha) = MONTH(CURRENT_DATE()) AND YEAR(Fecha) = YEAR(CURRENT_DATE())")
            mes = cursor.fetchone()[0]
            cursor.execute("""
                SELECT m.Nombre FROM alquiler a JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa 
                JOIN marca m ON v.ID_Marca = m.ID GROUP BY m.Nombre ORDER BY COUNT(*) DESC LIMIT 1
            """)
            res = cursor.fetchone()
            marca = res[0] if res else "N/A"
            
            # Consultar Mensual
            cursor.execute("""
                SELECT DATE_FORMAT(Fecha, '%Y-%m') as Mes, COUNT(*) as Total
                FROM alquiler GROUP BY Mes ORDER BY Mes ASC LIMIT 12
            """)
            mensual = cursor.fetchall()
            
            # Consultar Marcas
            cursor.execute("""
                SELECT m.Nombre, COUNT(a.COD_Alquiler)
                FROM alquiler a JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa
                JOIN marca m ON v.ID_Marca = m.ID GROUP BY m.Nombre
                ORDER BY COUNT(a.COD_Alquiler) DESC
            """)
            marcas = cursor.fetchall()
            
            cursor.close()
            return (total, mes, marca), mensual, marcas
        except mysql.connector.Error:
            self.reconnect_db()
            return (0, 0, "N/A"), [], []

    def reconnect_db(self):
        try:
            if self.mydb: self.mydb.close()
            self.mydb = mysql.connector.connect(
                host="localhost", user="root", password="123456",
                database="control_alquiler_Reych", autocommit=True
            )
        except: pass

    def actualizar_en_tiempo_real(self):
        if not self.winfo_exists(): return
        
        kpis_new, mensual_new, marcas_new = self.consultar_data()
        modo_new = get_appearance_mode()
        
        # 1. Actualizar KPIs (siempre, es barato y no parpadea)
        self.kpi_labels['total'].configure(text=str(kpis_new[0]))
        self.kpi_labels['mes'].configure(text=str(kpis_new[1]))
        self.kpi_labels['marca'].configure(text=kpis_new[2])
        
        # 2. Actualizar Gráficos (solo si hay cambios de datos o tema)
        if mensual_new != self.datos_mensuales or modo_new != self.ultimo_modo:
            self.datos_mensuales = mensual_new
            self.dibujar_linea_mensual()
            
        if marcas_new != self.datos_marcas or modo_new != self.ultimo_modo:
            self.datos_marcas = marcas_new
            self.dibujar_barras_marcas()
            
        self.ultimo_modo = modo_new
        self._after_id = self.after(10000, self.actualizar_en_tiempo_real)

    def setup_plot_theme(self, fig, ax):
        is_light = self.ultimo_modo == "Light"
        bg_color = "#FFFFFF" if is_light else "#1E1E1E"
        text_color = "#333333" if is_light else "#E0E0E0"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(text_color)
            spine.set_linewidth(0.5)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        return text_color

    def dibujar_linea_mensual(self):
        for w in self.container_mensual.winfo_children(): w.destroy()
        if not self.datos_mensuales:
            CTkLabel(self.container_mensual, text="Sin datos", text_color="gray").pack(pady=50)
            return

        meses = [d[0] for d in self.datos_mensuales]
        cantidades = [d[1] for d in self.datos_mensuales]

        fig = Figure(figsize=(5, 3.5), dpi=90)
        ax = fig.add_subplot(111)
        text_color = self.setup_plot_theme(fig, ax)
        
        line_color = "#00501B" if self.ultimo_modo == "Light" else "#00FF7F"
        ax.plot(meses, cantidades, marker='o', color=line_color, linewidth=2)
        ax.set_title("Alquileres por Mes", fontsize=12, fontweight="bold")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(True, linestyle='--', alpha=0.3, color=text_color)

        canvas = FigureCanvasTkAgg(fig, master=self.container_mensual)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=BOTH, padx=10, pady=10)

    def dibujar_barras_marcas(self):
        for w in self.container_marcas.winfo_children(): w.destroy()
        if not self.datos_marcas:
            CTkLabel(self.container_marcas, text="Sin datos", text_color="gray").pack(pady=50)
            return

        marcas = [d[0] for d in self.datos_marcas]
        cantidades = [d[1] for d in self.datos_marcas]

        fig = Figure(figsize=(5, 3.5), dpi=90)
        ax = fig.add_subplot(111)
        self.setup_plot_theme(fig, ax)
        
        bar_color = "#00501B" if self.ultimo_modo == "Light" else "#00A86B"
        ax.bar(marcas, cantidades, color=bar_color)
        ax.set_title("Vehículos más alquilados", fontsize=12, fontweight="bold")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = FigureCanvasTkAgg(fig, master=self.container_marcas)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=BOTH, padx=10, pady=10)

    def actualizar_ahora(self):
        # Forzar actualización inmediata ignorando caché
        self.datos_mensuales = None
        self.datos_marcas = None
        self.actualizar_en_tiempo_real()

    def destroy(self):
        if self._after_id: self.after_cancel(self._after_id)
        if self.mydb.is_connected(): self.mydb.close()
        super().destroy()
