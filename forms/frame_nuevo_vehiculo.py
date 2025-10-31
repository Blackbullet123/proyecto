from customtkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import mysql.connector
from PIL import Image
import subprocess
import datetime
import os

class FrameNuevoVehiculo(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123456",
            port = "3306",
            database = "control_alquiler_Reych"
        )

        my_cursor = mydb.cursor()

        def query_db():
                conn = mydb

                my_cursor = mydb.cursor()

                my_cursor.execute("SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca")
                records = my_cursor.fetchall()

                count = 0

                for record in records:
                    if count % 2 == 0:
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('evenrow',))
                    else: 
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('oddrow',))

                    count += 1

                conn.commit()
                conn.close()
                conn.close()

        def actualizar_tree():
            for item in my_tree.get_children():
                my_tree.delete(item)

                mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                port = "3306",
                database = "control_alquiler_Reych"
            )

            conn = mydb

            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca")
            records = my_cursor.fetchall()

            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('evenrow',))
                else: 
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('oddrow',))

                count += 1

            conn.commit()
            conn.close()

        style = ttk.Style()

        style.theme_use('clam')

        style.configure(
            "Treeview",
            background="lightgreen",
            foreground="black",
            rowheight=25,
            fieldbackground="#FCFCFC"
        )

        style.map('Treeview',
                background=[('selected',"#003d3c")])
        
        def agregar():
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                port = "3306",
                database = "control_alquiler_Reych"
            )

            my_cursor = mydb.cursor()

            sql3 = '''INSERT INTO vehiculo (Placa, Color, Año, ID_Marca) VALUES (%s,%s,%s,%s)'''
            values3 = (placa_entry.get(), color_entry.get(), año_entry.get(), codigo_marca.get())
            try:
                my_cursor.execute(sql3, values3)
                mydb.commit()

                if self.ruta_imagen_seleccionada:
                    carpeta_destino = "imagenes_vehiculos"
                    if not os.path.exists(carpeta_destino):
                        os.makedirs(carpeta_destino)

                    nombre_archivo = f"{placa_entry.get()}.jpg"
                    ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
                    from shutil import copyfile
                    copyfile(self.ruta_imagen_seleccionada, ruta_destino)

                titulo = 'Ingreso'
                mensaje = 'Vehículo agregado con éxito'
                messagebox.showinfo(titulo, mensaje)
            except Exception as e:
                titulo = 'Error'
                mensaje = f'Ocurrió un problema: {e}'
                messagebox.showerror(titulo, mensaje)
            finally:
                mydb.close()
                actualizar_tree()
                # Limpia campos
                codigo_marca.delete(0, END)
                placa_entry.delete(0, END)
                color_entry.delete(0, END)
                año_entry.delete(0, END)
                self.ruta_imagen_seleccionada = None


        def eliminar():
            mydb = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "123456",
                        port = "3306",
                        database = "control_alquiler_Reych"
                    )

            my_cursor = mydb.cursor()

            #sql = "DELETE FROM marca WHERE ID = '{0}'"
            #sql2 = "DELETE FROM modelo WHERE ID_Marca = '{0}'"
            sql3 = "DELETE FROM vehiculo WHERE Placa = '{0}'"
            try:
                my_cursor.execute(sql3.format(placa_entry.get()))
                mydb.commit()
                #conn.close()
                #my_cursor.execute(sql2.format(codigo_marca.get()))
                #mydb.commit()
                #conn.close()
                #my_cursor.execute(sql.format(codigo_marca.get()))
                #mydb.commit()
                titulo = 'Ingresión'
                mensaje = 'Vehiculo eliminado con exito'
                messagebox.showinfo(titulo, mensaje)
            except:
                titulo = 'Alquilado'
                mensaje = 'Ocurrio un problema'
                messagebox.showinfo(titulo, mensaje)
            finally:
                    actualizar_tree()

        def select_record(e):
            codigo_marca.delete(0,END)
            #nombre_marca.delete(0,END)
            #nombre_modelo.delete(0,END)
            placa_entry.delete(0,END)
            color_entry.delete(0,END)
            año_entry.delete(0,END)

            selected = my_tree.focus()
            values = my_tree.item(selected,'values')

            codigo_marca.insert(0,values[0])
            #nombre_marca.insert(0, values[1])
            #nombre_modelo.insert(0, values[2])
            placa_entry.insert(0, values[1])
            color_entry.insert(0, values[4])
            año_entry.insert(0, values[5])
            mostrar_imagen(values[1])


        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)

        titulo = CTkLabel(frame_superior, text="Nuevo Vehículo",
                        text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 5), pady=5)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                    selectmode="extended", show="headings")
        my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=my_tree.yview)

        frame_barra_derecha = CTkFrame(tabla_contenedor, fg_color="#000000", corner_radius=10)
        frame_barra_derecha.pack(side=RIGHT, fill=Y, padx=(5, 10), pady=5)

        self.img_label = CTkLabel(frame_barra_derecha, text="Imagen")
        self.img_label.pack(pady=30, padx=10)

        alquilar = CTkButton(frame_barra_derecha, text="Agregar", fg_color="#00A86B", text_color="white")
        alquilar.pack(pady=5)

        limpiar = CTkButton(frame_barra_derecha, text="Eliminar", fg_color="#D32F2F",text_color="white")
        limpiar.pack(pady=5)

        frame_inferior = CTkFrame(self, fg_color="#EEEEEE", corner_radius=10)
        frame_inferior.pack(padx=20, pady=15, fill="x")

                # === Contenedor principal del formulario ===
        frame_contenedor_form = CTkFrame(frame_inferior, fg_color="transparent")
        frame_contenedor_form.pack(fill="x", pady=10, padx=10)

        # === Subframe: Campos de entrada ===
        frame_entry = CTkFrame(frame_contenedor_form, fg_color="transparent")
        frame_entry.pack(side="left", fill="both", expand=True, padx=(10, 5))

        # Campos de entrada
        cod_marca = CTkLabel(frame_entry, text="Código", text_color="black", font=("Ubuntu", 14))
        cod_marca.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        codigo_marca = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        codigo_marca.grid(row=0, column=1, padx=10, pady=10)

        placa_label = CTkLabel(frame_entry, text="Placa", text_color="black", font=("Ubuntu", 14))
        placa_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        placa_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        placa_entry.grid(row=0, column=3, padx=10, pady=10)

        color_label = CTkLabel(frame_entry, text="Color", text_color="black", font=("Ubuntu", 14))
        color_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        color_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        color_entry.grid(row=0, column=5, padx=10, pady=10)

        año_label = CTkLabel(frame_entry, text="Año", text_color="black", font=("Ubuntu", 14))
        año_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        año_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        año_entry.grid(row=1, column=1, padx=10, pady=10)

        marca_label = CTkLabel(frame_entry, text="Marca", text_color="black", font=("Ubuntu", 14))
        marca_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        marca_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        marca_entry.grid(row=1, column=3, padx=10, pady=10)

        modelo_label = CTkLabel(frame_entry, text="Modelo", text_color="black", font=("Ubuntu", 14))
        modelo_label.grid(row=1, column=4, padx=10, pady=10, sticky="e")
        modelo_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        modelo_entry.grid(row=1, column=5, padx=10, pady=10)

        # === Subframe: Imagen del vehículo (al lado derecho) ===
        frame_imagen = CTkFrame(frame_contenedor_form, fg_color="#DDDDDD", corner_radius=12)
        frame_imagen.pack(side="right", padx=(5, 10), pady=10, fill="y")

        CTkLabel(
            frame_imagen,
            text="Imagen del Vehículo",
            text_color="#00332B",
            font=("Ubuntu", 15, "bold")
        ).pack(pady=(10, 5))

        # Vista previa
        self.preview_label = CTkLabel(
            frame_imagen,
            text="Sin imagen",
            width=180,
            height=130,
            fg_color="#B0BEC5",
            corner_radius=8
        )
        self.preview_label.pack(pady=5, padx=10)

        self.ruta_imagen_seleccionada = None

        # Función para seleccionar imagen
        def seleccionar_imagen():
            ruta = filedialog.askopenfilename(
                title="Seleccionar imagen del vehículo",
                filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")]
            )
            if ruta:
                self.ruta_imagen_seleccionada = ruta
                imagen = Image.open(ruta)
                imagen = imagen.resize((180, 130))
                imagen_tk = CTkImage(light_image=imagen, dark_image=imagen, size=(180, 130))
                self.preview_label.configure(image=imagen_tk, text="")
                self.preview_label.image = imagen_tk

        btn_subir_img = CTkButton(
            frame_imagen,
            text="Seleccionar Imagen",
            fg_color="#00796B",
            hover_color="#004D40",
            text_color="white",
            font=("Ubuntu", 13, "bold"),
            height=35,
            command=seleccionar_imagen
        )
        btn_subir_img.pack(pady=(10, 15))


        my_tree['columns']=("ID","Placa","Marca","Modelo","Color", "Año")

        my_tree.column("ID",anchor=CENTER,width=120)
        my_tree.column("Placa",anchor=CENTER,width=120)
        my_tree.column("Marca",anchor=CENTER,width=120)
        my_tree.column("Modelo",anchor=CENTER,width=120)
        my_tree.column("Color",anchor=CENTER,width=120)
        my_tree.column("Año",anchor=CENTER,width=120)

        my_tree.heading("ID", text="COD",anchor=CENTER)
        my_tree.heading("Placa", text="Placa",anchor=CENTER)
        my_tree.heading("Marca", text="Vehiculo Marca",anchor=CENTER)
        my_tree.heading("Modelo", text="Vehiculo Modelo",anchor=CENTER)
        my_tree.heading("Color", text="Color",anchor=CENTER)
        my_tree.heading("Año", text="Año",anchor=CENTER)
                

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#5dc1b9")

        my_tree.bind("<ButtonRelease-1>", select_record)

        query_db()

        

        def mostrar_imagen(placa):
            try:
                carpeta_imagenes = "imagenes_vehiculos"
                ruta_imagen = os.path.join(carpeta_imagenes, f"{placa}.jpg")

                if not os.path.exists(ruta_imagen):
                    ruta_imagen = os.path.join(carpeta_imagenes, "default.jpg")
                    if not os.path.exists(ruta_imagen):
                        self.img_label.configure(image=None, text="Sin imagen")
                        return

                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((200, 150))
                imagen_tk = CTkImage(light_image=imagen, dark_image=imagen, size=(200, 150))
                self.img_label.configure(image=imagen_tk, text="")
                self.img_label.image = imagen_tk

            except Exception as e:
                print("Error al cargar imagen:", e)
                self.img_label.configure(image=None, text="Error")

        mostrar_imagen("default")
