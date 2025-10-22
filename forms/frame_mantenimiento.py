from customtkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image
import os

class FrameMantenimiento(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador

        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X)

        titulo = CTkLabel(frame_superior, text="MANTENIMIENTO",
                          text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60, side=RIGHT)
        
        frame_centro_container = CTkFrame(self, fg_color="#EEEEEE")
        frame_centro_container.pack(expand=True, fill=BOTH, pady=10)

        canvas = CTkCanvas(frame_centro_container, bg="#EEEEEE", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(frame_centro_container, orient="vertical", command=canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scroll.set)

        frame_centro = CTkFrame(canvas, fg_color="#EEEEEE")
        canvas.create_window((0, 0), window=frame_centro, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame_centro.bind("<Configure>", on_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

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
                SELECT v.Placa, m.Nombre AS Marca, o.Nombre AS Modelo
                FROM vehiculo v
                INNER JOIN marca m ON v.ID_Marca = m.ID
                INNER JOIN modelo o ON o.ID_Marca = m.ID
            """)
            vehiculos = cursor.fetchall()
            mydb.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
            vehiculos = []

        columnas = 4
        fila_frame = None

        if not vehiculos:
            CTkLabel(frame_centro, text="No hay vehículos disponibles",
                     text_color="gray", font=("Ubuntu", 18, "bold")).pack(pady=40)
            return

        for i, (placa, marca, modelo) in enumerate(vehiculos):
            if i % columnas == 0:
                fila_frame = CTkFrame(frame_centro, fg_color="#EEEEEE")
                fila_frame.pack(fill=X, pady=10)

            card = CTkFrame(fila_frame, corner_radius=10, fg_color="white",
                            border_width=1, border_color="#00501B")
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

            CTkLabel(card, text=f"Marca: {marca}", font=("Ubuntu", 15), text_color="#00501B").pack(pady=1)
            CTkLabel(card, text=f"Modelo: {modelo}", font=("Ubuntu", 14), text_color="black").pack(pady=1)
            CTkLabel(card, text=f"Placa: {placa}", font=("Ubuntu", 14, "bold"), text_color="#00A86B").pack(pady=1)


            botones_frame = CTkFrame(card, fg_color="white")
            botones_frame.pack(pady=5)

            CTkButton(botones_frame, text="Verificar",
                      fg_color="#00501B", text_color="white",
                      width=110, height=25,
                      command=lambda p=placa: self.verificar_mantenimiento(p)
                      ).pack(side=LEFT, padx=5)

            CTkButton(botones_frame, text="Registrar",
                      fg_color="black", text_color="white",
                      width=110, height=25,
                      command=lambda p=placa: self.registrar_mantenimiento(p)
                      ).pack(side=LEFT, padx=5)


    def verificar_mantenimiento(self, placa):
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
            estado = "✅ Al día" if dias_pasados < 60 else "⚠️ Requiere revisión"

            messagebox.showinfo("Estado de mantenimiento",
                                f"Vehículo: {placa}\n"
                                f"Último mantenimiento: {fecha}\n"
                                f"Kilometraje: {km} km\n"
                                f"Descripción: {desc}\n"
                                f"Estado: {estado}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo consultar la base de datos:\n{err}")


    def registrar_mantenimiento(self, placa):
        ventana = CTkToplevel(self)
        ventana.title(f"Registrar mantenimiento - {placa}")
        ventana.geometry("400x400")
        ventana.grab_set()

        CTkLabel(ventana, text=f"Registrar mantenimiento para {placa}",
                 font=("Ubuntu", 16, "bold"), text_color="#00501B").pack(pady=10)

        fecha_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        km_var = StringVar()
        desc_var = StringVar()
        costo_var = StringVar()

        CTkLabel(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=(10, 0))
        fecha_entry = CTkEntry(ventana, textvariable=fecha_var, width=250, state=DISABLED)
        fecha_entry.pack()

        CTkLabel(ventana, text="Kilometraje actual:").pack(pady=(10, 0))
        km_entry = CTkEntry(ventana, textvariable=km_var, width=250)
        km_entry.pack()

        CTkLabel(ventana, text="Descripción:").pack(pady=(10, 0))
        desc_entry = CTkEntry(ventana, textvariable=desc_var, width=250)
        desc_entry.pack()

        CTkLabel(ventana, text="Costo (opcional):").pack(pady=(10, 0))
        costo_entry = CTkEntry(ventana, textvariable=costo_var, width=250)
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
                ventana.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error al guardar", f"No se pudo registrar:\n{err}")

        CTkButton(ventana, text="Guardar", fg_color="#00501B",
                  text_color="white", width=200, command=guardar).pack(pady=20)
