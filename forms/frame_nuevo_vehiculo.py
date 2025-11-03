from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from PIL import Image
from shutil import copyfile
import os

class FrameNuevoVehiculo(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador
        self.ruta_imagen_seleccionada = None

        # --- Conexión base de datos ---
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            port="3306",
            database="control_alquiler_Reych"
        )

        # --- Frames y títulos ---
        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)
        titulo = CTkLabel(frame_superior, text="Nuevo Vehículo", text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        # --- Contenedor tabla y barra derecha ---
        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        # --- Treeview ---
        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,5), pady=5)

        # --- Campo de búsqueda ---
        busqueda_label = CTkLabel(frame_superior, text="Buscar:", text_color="black", font=("Ubuntu", 14))
        busqueda_label.pack(side=LEFT, padx=(20,5))

        self.busqueda_entry = CTkEntry(frame_superior, width=200, fg_color="#c1e3f1", text_color="black")
        self.busqueda_entry.pack(side=LEFT, padx=(0,10))

        btn_buscar = CTkButton(frame_superior, text="Buscar", fg_color="#00796B", text_color="white",
                            command=self.buscar)
        btn_buscar.pack(side=LEFT, padx=(0,20))


        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", show="headings")
        self.my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("ID","Placa","Marca","Modelo","Color","Año")
        for col, width in zip(self.my_tree['columns'], [120]*6):
            self.my_tree.column(col, anchor=CENTER, width=width)

        self.my_tree.heading("ID", text="COD", anchor=CENTER)
        self.my_tree.heading("Placa", text="Placa", anchor=CENTER)
        self.my_tree.heading("Marca", text="Vehiculo Marca", anchor=CENTER)
        self.my_tree.heading("Modelo", text="Vehiculo Modelo", anchor=CENTER)
        self.my_tree.heading("Color", text="Color", anchor=CENTER)
        self.my_tree.heading("Año", text="Año", anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#5dc1b9")
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)

        # --- Barra derecha ---
        frame_barra_derecha = CTkFrame(tabla_contenedor, fg_color="#000000", corner_radius=10)
        frame_barra_derecha.pack(side=RIGHT, fill=Y, padx=(5,10), pady=5)

        self.img_label = CTkLabel(frame_barra_derecha, text="Imagen")
        self.img_label.pack(pady=30, padx=10)

        btn_agregar = CTkButton(frame_barra_derecha, text="Agregar", fg_color="#00A86B", text_color="white", command=self.agregar)
        btn_agregar.pack(pady=5)
        btn_eliminar = CTkButton(frame_barra_derecha, text="Eliminar", fg_color="#D32F2F", text_color="white", command=self.eliminar)
        btn_eliminar.pack(pady=5)

        # --- Formulario inferior ---
        frame_inferior = CTkFrame(self, fg_color="#EEEEEE", corner_radius=10)
        frame_inferior.pack(padx=20, pady=15, fill="x")

        frame_contenedor_form = CTkFrame(frame_inferior, fg_color="transparent")
        frame_contenedor_form.pack(fill="x", pady=10, padx=10)

        # --- Campos de entrada ---
        frame_entry = CTkFrame(frame_contenedor_form, fg_color="transparent")
        frame_entry.pack(side="left", fill="both", expand=True, padx=(10,5))

        # Código y Placa
        CTkLabel(frame_entry, text="Código", text_color="black", font=("Ubuntu",14)).grid(row=0,column=0,padx=10,pady=10,sticky="e")
        self.codigo_marca = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.codigo_marca.grid(row=0,column=1,padx=10,pady=10)

        CTkLabel(frame_entry, text="Placa", text_color="black", font=("Ubuntu",14)).grid(row=0,column=2,padx=10,pady=10,sticky="e")
        self.placa_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.placa_entry.grid(row=0,column=3,padx=10,pady=10)

        CTkLabel(frame_entry, text="Color", text_color="black", font=("Ubuntu",14)).grid(row=0,column=4,padx=10,pady=10,sticky="e")
        self.color_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.color_entry.grid(row=0,column=5,padx=10,pady=10)

        # Año, Marca, Modelo
        CTkLabel(frame_entry, text="Año", text_color="black", font=("Ubuntu",14)).grid(row=1,column=0,padx=10,pady=10,sticky="e")
        self.año_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.año_entry.grid(row=1,column=1,padx=10,pady=10)

        CTkLabel(frame_entry, text="Marca", text_color="black", font=("Ubuntu",14)).grid(row=1,column=2,padx=10,pady=10,sticky="e")
        self.marca_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.marca_entry.grid(row=1,column=3,padx=10,pady=10)

        CTkLabel(frame_entry, text="Modelo", text_color="black", font=("Ubuntu",14)).grid(row=1,column=4,padx=10,pady=10,sticky="e")
        self.modelo_entry = CTkEntry(frame_entry, fg_color="#c1e3f1", text_color="black", border_color="#002950", width=130)
        self.modelo_entry.grid(row=1,column=5,padx=10,pady=10)

        # --- Imagen ---
        frame_imagen = CTkFrame(frame_contenedor_form, fg_color="#DDDDDD", corner_radius=12)
        frame_imagen.pack(side="right", padx=(5,10), pady=10, fill="y")
        CTkLabel(frame_imagen, text="Imagen del Vehículo", text_color="#00332B", font=("Ubuntu",15,"bold")).pack(pady=(10,5))

        self.preview_label = CTkLabel(frame_imagen, text="Sin imagen", width=180, height=130, fg_color="#B0BEC5", corner_radius=8)
        self.preview_label.pack(pady=5,padx=10)

        btn_subir_img = CTkButton(frame_imagen, text="Seleccionar Imagen", fg_color="#00796B", hover_color="#004D40",
                                  text_color="white", font=("Ubuntu",13,"bold"), height=35,
                                  command=self.seleccionar_imagen)
        btn_subir_img.pack(pady=(10,15))

        # --- Cargar datos en Treeview ---
        self.query_db()

    # ======================= Funciones =======================

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen del vehículo",
            filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")]
        )
        if ruta:
            self.ruta_imagen_seleccionada = ruta
            imagen = Image.open(ruta)
            imagen = imagen.resize((180, 130))
            imagen_tk = CTkImage(light_image=imagen, dark_image=imagen, size=(180,130))
            self.preview_label.configure(image=imagen_tk, text="")
            self.preview_label.image = imagen_tk

    def query_db(self):
        my_cursor = self.mydb.cursor()
        my_cursor.execute(
            "SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año "
            "FROM vehiculo v "
            "LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa "
            "RIGHT JOIN marca m ON m.ID = v.ID_Marca "
            "INNER JOIN modelo o ON m.ID = o.ID_Marca"
        )
        records = my_cursor.fetchall()
        self.actualizar_treeview(records)

    def buscar(self):
        termino = self.busqueda_entry.get().strip()
        my_cursor = self.mydb.cursor()

        sql = ("SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año "
            "FROM vehiculo v "
            "LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa "
            "RIGHT JOIN marca m ON m.ID = v.ID_Marca "
            "INNER JOIN modelo o ON m.ID = o.ID_Marca "
            "WHERE v.Placa LIKE %s OR m.Nombre LIKE %s OR o.Nombre LIKE %s")
        like_termino = f"%{termino}%"
        my_cursor.execute(sql, (like_termino, like_termino, like_termino))
        records = my_cursor.fetchall()
        self.actualizar_treeview(records)


    def actualizar_treeview(self, records):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        count = 0
        for record in records:
            tag = 'evenrow' if count%2==0 else 'oddrow'
            self.my_tree.insert(parent='', index='end', iid=count, text='', values=record, tags=(tag,))
            count +=1

    def actualizar_tree(self):
        my_cursor = self.mydb.cursor()
        my_cursor.execute(
            "SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año "
            "FROM vehiculo v "
            "LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa "
            "RIGHT JOIN marca m ON m.ID = v.ID_Marca "
            "INNER JOIN modelo o ON m.ID = o.ID_Marca"
        )
        records = my_cursor.fetchall()
        self.actualizar_treeview(records)

    def agregar(self):
        my_cursor = self.mydb.cursor()

        # Insertar Marca si no existe
        my_cursor.execute("SELECT * FROM marca WHERE ID=%s", (self.codigo_marca.get(),))
        if not my_cursor.fetchone():
            my_cursor.execute("INSERT INTO marca (ID, Nombre) VALUES (%s,%s)",
                              (self.codigo_marca.get(), self.marca_entry.get()))
            self.mydb.commit()

        # Insertar Modelo si no existe
        my_cursor.execute("SELECT * FROM modelo WHERE Nombre=%s AND ID_Marca=%s",
                          (self.modelo_entry.get(), self.codigo_marca.get()))
        if not my_cursor.fetchone():
            my_cursor.execute("INSERT INTO modelo (Nombre, ID_Marca) VALUES (%s,%s)",
                              (self.modelo_entry.get(), self.codigo_marca.get()))
            self.mydb.commit()

        # Insertar Vehículo
        try:
            my_cursor.execute("INSERT INTO vehiculo (Placa, Color, Año, ID_Marca) VALUES (%s,%s,%s,%s)",
                              (self.placa_entry.get(), self.color_entry.get(), self.año_entry.get(), self.codigo_marca.get()))
            self.mydb.commit()

            # Guardar imagen
            if self.ruta_imagen_seleccionada:
                carpeta_destino = "imagenes_vehiculos"
                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)
                nombre_archivo = f"{self.placa_entry.get()}.jpg"
                ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
                copyfile(self.ruta_imagen_seleccionada, ruta_destino)

            messagebox.showinfo("Ingreso", "Vehículo agregado con éxito")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        finally:
            self.actualizar_tree()
            # Limpiar campos
            self.codigo_marca.delete(0, END)
            self.placa_entry.delete(0, END)
            self.color_entry.delete(0, END)
            self.año_entry.delete(0, END)
            self.marca_entry.delete(0, END)
            self.modelo_entry.delete(0, END)
            self.ruta_imagen_seleccionada = None

    def eliminar(self):
        my_cursor = self.mydb.cursor()
        try:
            my_cursor.execute("DELETE FROM vehiculo WHERE Placa=%s", (self.placa_entry.get(),))
            self.mydb.commit()
            messagebox.showinfo("Eliminación", "Vehículo eliminado con éxito")
        except:
            messagebox.showinfo("Error", "Ocurrió un problema al eliminar")
        finally:
            self.actualizar_tree()

    def select_record(self, e):
        selected = self.my_tree.focus()
        if selected:
            values = self.my_tree.item(selected, 'values')
            self.codigo_marca.delete(0, END)
            self.placa_entry.delete(0, END)
            self.color_entry.delete(0, END)
            self.año_entry.delete(0, END)
            self.marca_entry.delete(0, END)
            self.modelo_entry.delete(0, END)

            self.codigo_marca.insert(0, values[0])
            self.placa_entry.insert(0, values[1])
            self.marca_entry.insert(0, values[2])
            self.modelo_entry.insert(0, values[3])
            self.color_entry.insert(0, values[4])
            self.año_entry.insert(0, values[5])

            self.mostrar_imagen(values[1])

    def mostrar_imagen(self, placa):
        try:
            carpeta_imagenes = "imagenes_vehiculos"
            ruta_imagen = os.path.join(carpeta_imagenes, f"{placa}.jpg")
            if not os.path.exists(ruta_imagen):
                ruta_imagen = os.path.join(carpeta_imagenes, "default.jpg")
                if not os.path.exists(ruta_imagen):
                    self.img_label.configure(image=None, text="Sin imagen")
                    return
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((200,150))
            imagen_tk = CTkImage(light_image=imagen, dark_image=imagen, size=(200,150))
            self.img_label.configure(image=imagen_tk, text="")
            self.img_label.image = imagen_tk
        except Exception as e:
            print("Error al cargar imagen:", e)
            self.img_label.configure(image=None, text="Error")