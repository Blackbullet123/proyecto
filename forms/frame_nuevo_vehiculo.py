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

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            port="3306",
            database="control_alquiler_Reych"
        )

        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)

        titulo = CTkLabel(frame_superior, text="Nuevo Vehículo", text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=5, padx=60, side=RIGHT)

        CTkLabel(frame_superior, text="Buscar:", text_color="black", font=("Ubuntu", 14)).pack(side=LEFT, padx=(20,5))
        self.busqueda_entry = CTkEntry(frame_superior, width=250)
        self.busqueda_entry.pack(side=LEFT, padx=(0,10))

        btn_buscar = CTkButton(frame_superior, text="Buscar", font=("Ubuntu",13),
                               fg_color="#0E0F0F", text_color="white",
                               width=100, height=30)
        btn_buscar.pack(side=LEFT, padx=(0,20))

        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, anchor="center", expand=True, padx=(10,5), pady=5)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", show="headings")
        self.my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("Placa","Marca","Modelo","Color","Año")
        for col, width in zip(self.my_tree['columns'], [130]*5):
            self.my_tree.column(col, anchor=CENTER, width=width)
            self.my_tree.heading(col, text=col, anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#C8E6C9")

        barra_inferior = CTkFrame(self, fg_color="#004D40", corner_radius=0, height=120)
        barra_inferior.pack(side="bottom", fill="x", pady=(10,0))

        frame_campos = CTkFrame(barra_inferior, fg_color="transparent")
        frame_campos.pack(side="left", padx=15, pady=10)

        CTkLabel(frame_campos, text="Placa:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=0, padx=(5,2), sticky="e")
        self.placa_entry = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                    border_color="#00501B", width=120, height=28)
        self.placa_entry.grid(row=0, column=1, padx=(0,8))

        CTkLabel(frame_campos, text="Color:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=2, padx=(5,2), sticky="e")
        self.color_entry = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                    border_color="#00501B", width=120, height=28)
        self.color_entry.grid(row=0, column=3, padx=(0,8))

        CTkLabel(frame_campos, text="Año:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=4, padx=(5,2), sticky="e")
        self.año_entry = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                  border_color="#00501B", width=120, height=28)
        self.año_entry.grid(row=0, column=5, padx=(0,8))

        CTkLabel(frame_campos, text="Marca:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=6, padx=(5,2), sticky="e")
        self.marca_entry = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                    border_color="#00501B", width=120, height=28)
        self.marca_entry.grid(row=0, column=7, padx=(0,8))

        CTkLabel(frame_campos, text="Modelo:", text_color="white", font=("Ubuntu",13,"bold")).grid(row=0, column=8, padx=(5,2), sticky="e")
        self.modelo_entry = CTkEntry(frame_campos, fg_color="#c2f1c1", text_color="black",
                                     border_color="#00501B", width=120, height=28)
        self.modelo_entry.grid(row=0, column=9, padx=(0,8))

        frame_imagen = CTkFrame(barra_inferior, fg_color="#00695C", corner_radius=8)
        frame_imagen.pack(side="left", padx=15, pady=5)

        self.img_label = CTkLabel(frame_imagen, text="Sin imagen", width=130, height=80,
                                  fg_color="#B0BEC5", corner_radius=8)
        self.img_label.pack(padx=5, pady=3)

        btn_imagen = CTkButton(frame_imagen, text="Seleccionar", width=120, height=30,
                               fg_color="#00BFA5", hover_color="#009688",
                               text_color="white", font=("Ubuntu",12,"bold"),
                               )
        btn_imagen.pack(pady=(0,5))

        frame_botones = CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=(0,10))

        btn_agregar = CTkButton(frame_botones, text="Agregar",
                                fg_color="#00C853", hover_color="#00E676",
                                text_color="white", font=("Ubuntu",13,"bold"),
                                width=120)
        btn_agregar.grid(row=0, column=0, padx=15, pady=5)

        self.limpiar = CTkButton(frame_botones, text="Limpiar", fg_color="#FFA000",
                                hover_color="#FFB300", text_color="white",
                                font=("Ubuntu",13,"bold"), width=120)
        self.limpiar.grid(row=0, column=1, padx=15, pady=5)

        btn_eliminar = CTkButton(frame_botones, text="Eliminar",
                                 fg_color="#D32F2F", hover_color="#E53935",
                                 text_color="white", font=("Ubuntu",13,"bold"),
                                 width=120)
        btn_eliminar.grid(row=0, column=2, padx=15, pady=5)

