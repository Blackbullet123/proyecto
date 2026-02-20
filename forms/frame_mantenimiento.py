from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox, Tk
from datetime import datetime
import mysql.connector
from PIL import Image
import os

class FrameMantenimiento(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=('#EEEEEE', '#1A1A1A'))

        self.controlador = controlador

        self.COLOR_MANTENIMIENTO_ATRASADO = "#FF3B30" 
        self.COLOR_SIN_REGISTRO = "#007AFF"         
        self.COLOR_OPTIMO = "#34C759" 

        frame_superior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))
        frame_superior.pack(pady=10, fill=X)


        titulo = CTkLabel(frame_superior, text="MANTENIMIENTO",
                          text_color=("#00501B", "#00FF7F"), font=("Impact", 45))
        titulo.pack(pady=0, padx=20, side=RIGHT)


        frame_centro_container = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))
        frame_centro_container.pack(expand=True, fill=BOTH, pady=10)


        bg_color = "#EEEEEE" if get_appearance_mode() == "Light" else "#1A1A1A"
        self.canvas = CTkCanvas(frame_centro_container, bg=bg_color, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)


        scroll = ttk.Scrollbar(frame_centro_container, orient="vertical", command=self.canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scroll.set)

        self.frame_centro = CTkFrame(self.canvas, fg_color=("#EEEEEE", "#1A1A1A"))

        self.canvas.create_window((0, 0), window=self.frame_centro, anchor="nw")

        frame_leyenda = CTkFrame(frame_superior, fg_color="transparent")
        frame_leyenda.pack(side=LEFT, padx=20)
        self.legend_canvases = []

        def crear_item_leyenda(parent, color, texto):
            item = CTkFrame(parent, fg_color="transparent")
            item.pack(side=LEFT, padx=10)

            # Usamos colores dinámicos para el fondo del mini canvas de la leyenda
            bg_item = "#EEEEEE" if get_appearance_mode() == "Light" else "#1A1A1A"
            canvas = CTkCanvas(item, width=14, height=14, bg=bg_item, highlightthickness=0)
            canvas.pack(side=LEFT)
            self.legend_canvases.append(canvas)

            canvas.create_oval(2, 2, 12, 12, fill=color, outline=color)

            CTkLabel(
                item,
                text=texto,
                font=("Ubuntu", 13, "bold"),
                text_color=("black", "white")
            ).pack(side=LEFT, padx=6)


        crear_item_leyenda(frame_leyenda, self.COLOR_MANTENIMIENTO_ATRASADO, "Mantenimiento necesario")
        crear_item_leyenda(frame_leyenda, self.COLOR_SIN_REGISTRO, "Sin registro")
        crear_item_leyenda(frame_leyenda, self.COLOR_OPTIMO, "Óptimas condiciones")


        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.frame_centro.bind("<Configure>", on_configure)

        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.cargar_vehiculos()

    def actualizar_ahora(self):
        """Fuerza un refresco inmediato de la interfaz para actualizar colores de canvas"""
        bg_color = "#EEEEEE" if get_appearance_mode() == "Light" else "#1A1A1A"
        
        # Actualizar canvas principal
        self.canvas.configure(bg=bg_color)
        
        # Actualizar mini-canvases de la leyenda
        for leg_canvas in getattr(self, 'legend_canvases', []):
            leg_canvas.configure(bg=bg_color)

        # Actualizar marcadores de estado en las tarjetas
        bg_card = "#FFFFFF" if get_appearance_mode() == "Light" else "#2B2B2B"
        for alert_canvas in getattr(self, 'vehicle_canvases', []):
            alert_canvas.configure(bg=bg_card)
            
        self.cargar_vehiculos()

    def cargar_vehiculos(self):
        for widget in self.frame_centro.winfo_children():
            widget.destroy()
        self.vehicle_canvases = []

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                port="3306",
                database="control_alquiler_Reych"
            )
            cursor = mydb.cursor()
            cursor.execute("""
                SELECT v.Placa, m.Nombre AS Marca, o.Nombre AS Modelo, v.dias_mantenimiento
                FROM vehiculo v
                INNER JOIN marca m ON v.ID_Marca = m.ID
                INNER JOIN modelo o ON v.ID_Modelo = o.ID
            """)
            vehiculos = cursor.fetchall()
            mydb.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
            vehiculos = []

        columnas = 4
        fila_frame = None

        if not vehiculos:
            CTkLabel(self.frame_centro, text="No hay vehículos disponibles",
                     text_color="gray", font=("Ubuntu", 18, "bold")).pack(pady=40)
            return

        for i, (placa, marca, modelo, dias_mantenimiento) in enumerate(vehiculos):
            if i % columnas == 0:
                fila_frame = CTkFrame(self.frame_centro, fg_color=("#EEEEEE", "#1A1A1A"))
                fila_frame.pack(fill=X, pady=10)

            card = CTkFrame(fila_frame, corner_radius=10, fg_color=("#FFFFFF", "#2B2B2B"),
                            border_width=1, border_color=("#00501B", "#00FF7F"))

            card.pack(side=LEFT, padx=20, pady=10, expand=True, fill=BOTH)

            ruta_imagen = f"imagenes_vehiculos/{placa}.jpg"
            if not os.path.exists(ruta_imagen):
                ruta_imagen = "imagenes_vehiculos/default.jpg"
            try:
                img = Image.open(ruta_imagen).resize((200, 140))
                photo = CTkImage(light_image=img, dark_image=img, size=(200, 140))
                CTkLabel(card, image=photo, text="").pack(pady=5)
            except Exception:
                CTkLabel(card, text="Sin imagen", text_color="gray").pack(pady=5)

            CTkLabel(card, text=f"Marca: {marca}", font=("Ubuntu", 15), text_color=("#00501B", "#00FF7F")).pack(pady=1)
            CTkLabel(card, text=f"Modelo: {modelo}", font=("Ubuntu", 14), text_color=("black", "white")).pack(pady=1)
            CTkLabel(card, text=f"Placa: {placa}", font=("Ubuntu", 14, "bold"), text_color=("#00A86B", "#00FF7F")).pack(pady=1)


            color_marcador = self.obtener_color_marcador(placa, dias_mantenimiento)
            if color_marcador:
                # Determinamos el color de fondo manualmente ya que CTkCanvas no acepta tuplas de color
                bg_card = "#FFFFFF" if get_appearance_mode() == "Light" else "#2B2B2B"
                alert_canvas = CTkCanvas(card, width=20, height=20, bg=bg_card, highlightthickness=0)
                alert_canvas.place(relx=1.0, y=5, anchor="ne")
                alert_canvas.create_oval(2, 2, 18, 18, fill=color_marcador, outline=color_marcador)
                self.vehicle_canvases.append(alert_canvas)

            botones_superior = CTkFrame(card, fg_color="transparent")

            botones_superior.pack(pady=5)
            CTkButton(botones_superior, text="Verificar",
                      fg_color="#00501B", text_color="white",
                      width=110, height=25,
                      command=lambda p=placa, d=dias_mantenimiento: self.verificar_mantenimiento(p, d)
                      ).pack(side=LEFT, padx=5)
            CTkButton(botones_superior, text="Registrar",
                      fg_color="black", text_color="white",
                      width=110, height=25,
                      command=lambda p=placa: self.registrar_mantenimiento(p)
                      ).pack(side=LEFT, padx=5)

            botones_inferior = CTkFrame(card, fg_color="transparent")

            botones_inferior.pack(pady=5)
            CTkButton(botones_inferior, text="Configurar",
                      fg_color="#FFA500", text_color="white",
                      width=110, height=25,
                      command=lambda p=placa: self.configurar_mantenimiento_vehiculo(p)
                      ).pack()

    def obtener_color_marcador(self, placa, dias_mantenimiento):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                port="3306",
                database="control_alquiler_Reych"
            )
            cursor = mydb.cursor()
            cursor.execute("""
                SELECT Fecha
                FROM mantenimiento
                WHERE Placa = %s
                ORDER BY Fecha DESC
                LIMIT 1
            """, (placa,))
            resultado = cursor.fetchone()
            mydb.close()

            if not resultado:
                return self.COLOR_SIN_REGISTRO

            fecha_ultimo = resultado[0]
            dias_pasados = (datetime.now().date() - fecha_ultimo).days
            dias_restantes = dias_mantenimiento - dias_pasados

            if dias_restantes <= 1:
                return self.COLOR_MANTENIMIENTO_ATRASADO
            else:
                return self.COLOR_OPTIMO

        except mysql.connector.Error as err:
            print(f"Error al obtener marcador de mantenimiento: {err}")
            return None

    def configurar_mantenimiento_vehiculo(self, placa):
        ventana = Toplevel(self)
        ventana.title(f"Configurar mantenimiento - {placa}")
        ventana.geometry("300x200+550+250")
        ventana.grab_set()

        CTkLabel(ventana, text="Cada cuántos días \n realizar mantenimiento?",text_color="#00501B",
                 font=("Ubuntu", 14, "bold")).pack(pady=20)

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                port="3306",
                database="control_alquiler_Reych"
            )
            cursor = mydb.cursor()
            cursor.execute("SELECT dias_mantenimiento FROM vehiculo WHERE Placa = %s", (placa,))
            resultado = cursor.fetchone()
            mydb.close()
            dias_actual = resultado[0] if resultado else 30
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener la configuración:\n{err}")
            dias_actual = 30

        dias_var = StringVar(value=str(dias_actual))
        CTkEntry(ventana, textvariable=dias_var, width=100, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B").pack(pady=10)


        def guardar_config():
            try:
                dias = int(dias_var.get())
                if dias <= 0:
                    raise ValueError

                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456",
                    port="3306",
                    database="control_alquiler_Reych"
                )
                cursor = mydb.cursor()
                cursor.execute("UPDATE vehiculo SET dias_mantenimiento = %s WHERE Placa = %s", (dias, placa))
                mydb.commit()
                mydb.close()

                messagebox.showinfo("Éxito", f"Tiempo de mantenimiento configurado a {dias} días para {placa}")
                self.cargar_vehiculos()
                ventana.destroy()

            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido mayor a 0.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo guardar la configuración:\n{err}")

        CTkButton(ventana, text="Guardar", fg_color="#00501B", text_color="white",
                  command=guardar_config).pack(pady=20)

    def verificar_mantenimiento(self, placa, dias_mantenimiento):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                port="3306",
                database="control_alquiler_Reych"
            )
            cursor = mydb.cursor()
            cursor.execute("""
                SELECT Fecha, Kilometraje, Descripcion
                FROM mantenimiento WHERE Placa = %s
                ORDER BY Fecha DESC LIMIT 1
            """, (placa,))
            resultado = cursor.fetchone()
            mydb.close()

            if not resultado:
                messagebox.showwarning("Sin registro",
                                       f"El vehículo {placa} no tiene mantenimientos registrados.")
                return

            fecha, km, desc = resultado
            dias_pasados = (datetime.now().date() - fecha).days
            dias_faltantes = max(dias_mantenimiento - dias_pasados, 0)

            if dias_faltantes <= 1:
                estado = f"❌ Mantenimiento atrasado o próximo"
            else:
                estado = f"✅ Al día, faltan {dias_faltantes} días para el próximo mantenimiento"

            messagebox.showinfo("Estado de mantenimiento",
                                f"Vehículo: {placa}\n"
                                f"Último mantenimiento: {fecha}\n"
                                f"Kilometraje: {km} km\n"
                                f"Descripción: {desc}\n"
                                f"Estado: {estado}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo consultar la base de datos:\n{err}")

    def registrar_mantenimiento(self, placa):
        ventana = Toplevel(self)
        ventana.title(f"Registrar mantenimiento - {placa}")
        ventana.geometry("400x400+500+200")
        ventana.grab_set()

        CTkLabel(ventana, text=f"Registrar mantenimiento para {placa}",
                 font=("Ubuntu", 16, "bold"), text_color="#000000").pack(pady=10)

        fecha_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        km_var = StringVar()
        desc_var = StringVar()
        costo_var = StringVar()

        CTkLabel(ventana, text_color="#00501B",text="Kilometraje actual:").pack(pady=(10, 0))
        km_entry = CTkEntry(ventana, textvariable=km_var, width=250, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")

        km_entry.pack()

        CTkLabel(ventana, text_color="#00501B",text="Descripción:").pack(pady=(10, 0))
        desc_entry = CTkEntry(ventana, textvariable=desc_var, width=250, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")

        desc_entry.pack()

        CTkLabel(ventana, text_color="#00501B",text="Costo (opcional):").pack(pady=(10, 0))
        costo_entry = CTkEntry(ventana, textvariable=costo_var, width=250, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")

        costo_entry.pack()

        def guardar():
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456",
                    port="3306",
                    database="control_alquiler_Reych"
                )
                cursor = mydb.cursor()
                cursor.execute("""
                    INSERT INTO mantenimiento (Placa, Fecha, Kilometraje, Descripcion, Costo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (placa, fecha_var.get(), km_var.get(), desc_var.get(), costo_var.get() or None))
                mydb.commit()
                mydb.close()
                messagebox.showinfo("Éxito", f"Mantenimiento registrado para {placa}.")
                self.cargar_vehiculos() 
                ventana.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error al guardar", f"No se pudo registrar:\n{err}")

        CTkButton(ventana, text="Guardar", fg_color="#00501B", text_color="white",
                  command=guardar).pack(pady=20)
