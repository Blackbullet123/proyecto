from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring
import mysql.connector
from PIL import Image, ImageTk
import os
from shutil import copyfile

class FrameNuevoVehiculo(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador
        self.ruta_imagen_seleccionada = None

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            port="3306",
            database="control_alquiler_Reych"
        )
        self.mycursor = self.mydb.cursor()

        self.crear_ui()
        self.cargar_treeview()

    def entry_mayusculas(self, entry):
        text = entry.get()
        if text:
            cursor_pos = entry.index(tk.INSERT)
            new_text = text.upper()
            if new_text != text:
                entry.delete(0, tk.END)
                entry.insert(0, new_text)
                entry.icursor(cursor_pos)

    def convertir_mayusculas(self, texto):
        if texto:
            return texto.upper()
        return texto

    def crear_ui(self):
        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)
        
        CTkLabel(frame_superior, text="Nuevo Vehículo", text_color="#00501B",
                 font=("Impact", 45)).pack(pady=5, padx=60, side=RIGHT)
        CTkLabel(frame_superior, text="Buscar:", text_color="black",
                 font=("Ubuntu", 14)).pack(side=LEFT, padx=(20,5))
        self.busqueda_entry = CTkEntry(frame_superior, width=250)
        self.busqueda_entry.pack(side=LEFT, padx=(0,10))
        CTkButton(frame_superior, text="Buscar", font=("Ubuntu",13),
                  fg_color="#0E0F0F", text_color="white", width=100, height=30,
                  command=self.buscar_vehiculo).pack(side=LEFT, padx=(0,20))

        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, anchor="center", expand=True, padx=(10,5), pady=5)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse", show="headings")
        self.my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("Placa","Marca","Modelo","Color","Año")
        for col, width in zip(self.my_tree['columns'], [140]*5):

            self.my_tree.column(col, anchor=CENTER, width=width)
            self.my_tree.heading(col, text=col, anchor=CENTER)
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#00A86B")
        self.my_tree.bind("<ButtonRelease-1>", self.seleccionar_fila)

        barra_inferior = CTkFrame(self, fg_color="#004D40", corner_radius=0, height=120)
        barra_inferior.pack(side="bottom", fill="x", pady=(10,0))

        frame_campos = CTkFrame(barra_inferior, fg_color="transparent")
        frame_campos.pack(side="left", padx=15, pady=10)

        labels = ["Placa","Color","Año"]
        self.entries = {}
        for i, label in enumerate(labels):
            CTkLabel(frame_campos, text=f"{label}:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=i*2, padx=(5,2), sticky="e")
            self.entries[label.lower()] = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                                  border_color="#00501B", width=120, height=28)
            self.entries[label.lower()].grid(row=0, column=i*2+1, padx=(0,8))

        CTkLabel(frame_campos, text="Marca:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=6, padx=(5,2), sticky="e")
        self.marca_combobox = CTkComboBox(frame_campos,values=self.cargar_marcas(), width=120, command=self.actualizar_modelos)
        self.marca_combobox.grid(row=0, column=7, padx=(0,5))
        self.marca_combobox.set("")
        CTkButton(frame_campos, text="+", width=25, height=28, fg_color="#00BFA5",
                  hover_color="#009688", command=self.agregar_nueva_marca).grid(row=0, column=8, padx=(0,8))

        CTkLabel(frame_campos, text="Modelo:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=9, padx=(5,2), sticky="e")
        self.modelo_combobox = CTkComboBox(frame_campos, values=[], width=120)
        self.modelo_combobox.grid(row=0, column=10, padx=(0,5))
        self.modelo_combobox.set("")
        CTkButton(frame_campos, text="+", width=25, height=28, fg_color="#00BFA5",
                  hover_color="#009688", command=self.agregar_nuevo_modelo).grid(row=0, column=11, padx=(0,8))

        frame_imagen = CTkFrame(barra_inferior, fg_color="#00695C", corner_radius=8)
        frame_imagen.pack(side="left", padx=15, pady=5)
        self.img_label = CTkLabel(frame_imagen, text="Sin imagen", width=130, height=80,
                                  fg_color="#B0BEC5", corner_radius=8)
        self.img_label.pack(padx=5, pady=3)
        CTkButton(frame_imagen, text="Seleccionar", width=120, height=30,
                  fg_color="#00BFA5", hover_color="#009688", text_color="white", font=("Ubuntu",12,"bold"),
                  command=self.seleccionar_imagen).pack(pady=(0,5))

        frame_botones = CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=(0,10))
        CTkButton(frame_botones, text="Agregar", fg_color="#00C853", hover_color="#00E676",
                  text_color="white", font=("Ubuntu",13,"bold"), width=120, command=self.agregar_vehiculo).grid(row=0,column=0,padx=15,pady=5)
        CTkButton(frame_botones, text="Limpiar", fg_color="#FFA000", hover_color="#FFB300",
                  text_color="white", font=("Ubuntu",13,"bold"), width=120, command=self.limpiar_campos).grid(row=0,column=1,padx=15,pady=5)
        CTkButton(frame_botones, text="Eliminar", fg_color="#D32F2F", hover_color="#E53935",
                  text_color="white", font=("Ubuntu",13,"bold"), width=120, command=self.eliminar_vehiculo).grid(row=0,column=2,padx=15,pady=5)


        self.entries['placa'].bind("<KeyRelease>", lambda e: self.entry_mayusculas(self.entries['placa']))
        self.entries['color'].bind("<KeyRelease>", lambda e: self.entry_mayusculas(self.entries['color']))

    def cargar_marcas(self):
        self.mycursor.execute("SELECT Nombre FROM marca ORDER BY Nombre")
        return [m[0] for m in self.mycursor.fetchall()]

    def agregar_nueva_marca(self):
        nueva_marca = askstring("Nueva Marca", "Ingrese el nombre de la nueva marca:")
        if nueva_marca:
            nueva_marca = self.convertir_mayusculas(nueva_marca)
            self.mycursor.execute("SELECT * FROM marca WHERE Nombre=%s", (nueva_marca,))
            if self.mycursor.fetchone():
                messagebox.showerror("Error","La marca ya existe")
                return
            self.mycursor.execute("INSERT INTO marca (Nombre) VALUES (%s)", (nueva_marca,))
            self.mydb.commit()
            messagebox.showinfo("Éxito", f"Marca '{nueva_marca}' agregada")
            self.marca_combobox.configure(values=self.cargar_marcas())
            self.marca_combobox.set(nueva_marca)
            self.modelo_combobox.configure(values=[])

    def actualizar_modelos(self, marca_seleccionada):
        self.mycursor.execute("SELECT ID FROM marca WHERE Nombre=%s", (marca_seleccionada,))
        marca = self.mycursor.fetchone()
        if marca:
            id_marca = marca[0]
            self.mycursor.execute("SELECT Nombre FROM modelo WHERE ID_Marca=%s ORDER BY Nombre", (id_marca,))
            modelos = [m[0] for m in self.mycursor.fetchall()]
            self.modelo_combobox.configure(values=modelos)
            if modelos:
                self.modelo_combobox.set(modelos[0])
            else:
                self.modelo_combobox.set("")

    def agregar_nuevo_modelo(self):
        marca_seleccionada = self.marca_combobox.get()
        if not marca_seleccionada:
            messagebox.showerror("Error", "Seleccione primero una marca")
            return
        nuevo_modelo = askstring("Nuevo Modelo", "Ingrese el nombre del nuevo modelo:")
        if nuevo_modelo:
            nuevo_modelo = self.convertir_mayusculas(nuevo_modelo)
            self.mycursor.execute("SELECT ID FROM marca WHERE Nombre=%s", (marca_seleccionada,))
            marca = self.mycursor.fetchone()
            if not marca:
                messagebox.showerror("Error","La marca seleccionada no existe")
                return
            id_marca = marca[0]
            self.mycursor.execute("SELECT * FROM modelo WHERE Nombre=%s AND ID_Marca=%s", (nuevo_modelo, id_marca))
            if self.mycursor.fetchone():
                messagebox.showerror("Error","El modelo ya existe para esta marca")
                return
            self.mycursor.execute("INSERT INTO modelo (Nombre, ID_Marca) VALUES (%s,%s)", (nuevo_modelo, id_marca))
            self.mydb.commit()
            messagebox.showinfo("Éxito", f"Modelo '{nuevo_modelo}' agregado para la marca '{marca_seleccionada}'")
            self.actualizar_modelos(marca_seleccionada)
            self.modelo_combobox.set(nuevo_modelo)

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagenes","*.jpg *.png *.jpeg")])
        if ruta:
            self.ruta_imagen_seleccionada = ruta
            img = Image.open(ruta).resize((130,80))
            self.img_label.configure(image=ImageTk.PhotoImage(img))
            self.img_label.image = ImageTk.PhotoImage(img)

    def agregar_vehiculo(self):
        placa = self.entries['placa'].get().strip()
        color = self.entries['color'].get().strip()
        año = self.entries['año'].get().strip()
        marca_nombre = self.marca_combobox.get().strip()
        modelo_nombre = self.modelo_combobox.get().strip()

        if not placa or not color or not año or not marca_nombre or not modelo_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not self.ruta_imagen_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una imagen del vehículo antes de registrarlo")
            return

        self.mycursor.execute("SELECT * FROM vehiculo WHERE Placa=%s", (placa,))
        if self.mycursor.fetchone():
            messagebox.showerror("Error", "Ya existe un vehículo con esta placa")
            return

        self.mycursor.execute("SELECT ID FROM marca WHERE Nombre=%s", (marca_nombre,))
        marca = self.mycursor.fetchone()

        if not marca:
            self.mycursor.execute("INSERT INTO marca (Nombre) VALUES (%s)", (marca_nombre,))
            self.mydb.commit()
            self.mycursor.execute("SELECT ID FROM marca WHERE Nombre=%s", (marca_nombre,))
            marca = self.mycursor.fetchone()

        id_marca = marca[0]

        self.mycursor.execute("SELECT ID FROM modelo WHERE Nombre=%s AND ID_Marca=%s", (modelo_nombre, id_marca))
        modelo = self.mycursor.fetchone()

        if not modelo:
            self.mycursor.execute("INSERT INTO modelo (Nombre, ID_Marca) VALUES (%s, %s)", (modelo_nombre, id_marca))
            self.mydb.commit()
            self.mycursor.execute("SELECT ID FROM modelo WHERE Nombre=%s AND ID_Marca=%s", (modelo_nombre, id_marca))
            modelo = self.mycursor.fetchone()

        id_modelo = modelo[0]

        try:
            self.mycursor.execute("""
                INSERT INTO vehiculo (Placa, Color, Año, ID_Marca, ID_Modelo)
                VALUES (%s, %s, %s, %s, %s)
            """, (placa, color, año, id_marca, id_modelo))
            self.mydb.commit()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar el vehículo.\nDetalle: {str(e)}")
            return

        try:
            carpeta = "imagenes_vehiculos"
            os.makedirs(carpeta, exist_ok=True)
            ext = os.path.splitext(self.ruta_imagen_seleccionada)[1]
            destino = os.path.join(carpeta, f"{placa}{ext}")
            copyfile(self.ruta_imagen_seleccionada, destino)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen del vehículo.\nDetalle: {str(e)}")
            return

        messagebox.showinfo("Éxito", "Vehículo agregado correctamente")

        self.limpiar_campos()
        self.ruta_imagen_seleccionada = None
        self.cargar_treeview()

    def cargar_treeview(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        self.mycursor.execute("""
            SELECT v.Placa, m.Nombre, mo.Nombre, v.Color, v.Año
            FROM vehiculo v
            JOIN marca m ON v.ID_Marca = m.ID
            JOIN modelo mo ON v.ID_Modelo = mo.ID
        """)
        rows = self.mycursor.fetchall()
        for i, r in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.my_tree.insert('', 'end', values=r, tags=(tag,))

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.marca_combobox.set("")
        self.modelo_combobox.set("")
        self.img_label.configure(image="", text="Sin imagen")
        self.ruta_imagen_seleccionada = None
        self.cargar_treeview()

    def seleccionar_fila(self, event):
        seleccionado = self.my_tree.focus()
        if seleccionado:
            datos = self.my_tree.item(seleccionado, 'values')
            if datos:
                self.entries['placa'].delete(0, tk.END)
                self.entries['placa'].insert(0, datos[0])
                self.marca_combobox.set(datos[1])
                self.actualizar_modelos(datos[1])
                self.modelo_combobox.set(datos[2])
                self.entries['color'].delete(0, tk.END)
                self.entries['color'].insert(0, datos[3])
                self.entries['año'].delete(0, tk.END)
                self.entries['año'].insert(0, datos[4])

    def eliminar_vehiculo(self):
        seleccionado = self.my_tree.focus()
        if not seleccionado:
            messagebox.showerror("Error","Seleccione un vehículo")
            return
        placa = self.my_tree.item(seleccionado, 'values')[0]
        if messagebox.askyesno("Confirmar","¿Desea eliminar este vehículo?"):
            carpeta = "imagenes_vehiculos"
            if os.path.exists(carpeta):
                for archivo in os.listdir(carpeta):
                    nombre, ext = os.path.splitext(archivo)
                    if nombre == placa:
                        os.remove(os.path.join(carpeta, archivo))
                        break 

            self.mycursor.execute("DELETE FROM vehiculo WHERE Placa=%s",(placa,))
            self.mydb.commit()
            self.cargar_treeview()
            messagebox.showinfo("Éxito","Vehículo eliminado correctamente")
            self.limpiar_campos()

    def buscar_vehiculo(self):
        busqueda = self.busqueda_entry.get().strip()
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        query = """
            SELECT v.Placa, m.Nombre, mo.Nombre, v.Color, v.Año
            FROM vehiculo v
            JOIN marca m ON v.ID_Marca = m.ID
            JOIN modelo mo ON v.ID_Modelo = mo.ID
            WHERE v.Placa LIKE %s OR m.Nombre LIKE %s OR mo.Nombre LIKE %s
        """
        like = f"%{busqueda}%"
        self.mycursor.execute(query, (like, like, like))
        rows = self.mycursor.fetchall()
        for i, r in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.my_tree.insert('', 'end', values=r, tags=(tag,))
    