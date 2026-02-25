from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import mysql.connector
from customtkinter import *
from forms.imprimir_funcion import imprimir_historial
from PIL import Image

class FrameHistorial(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=("#EEEEEE", "#1A1A1A"))
        
        self.controlador = controlador

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            port="3306",
            database="control_alquiler_Reych"
        )
        self.my_cursor = self.mydb.cursor()

        # Top Section (Title and Print Button)
        frame_superior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))
        frame_superior.pack(fill=X, pady=10)

        titulo = CTkLabel(frame_superior, text="HISTORIAL DE VEHÍCULOS ELIMINADOS",
                          text_color=("#00501B", "#00FF7F"), font=("Impact", 35))
        titulo.pack(side=LEFT, padx=60)

        img = Image.open("imagenes/imprimir.png")
        img_white = Image.open("imagenes/imprimir_white.png")
        imprimir_icon_todo = CTkImage(light_image=img, dark_image=img_white, size=(30, 30))
        btn_imprimir = CTkButton(frame_superior, text=" Imprimir Reporte",
                                 fg_color="transparent", command=imprimir_historial,
                                 image=imprimir_icon_todo, hover_color="#00501B", text_color=("black", "white"),
                                 font=("Ubuntu", 18, "bold"))
        btn_imprimir.pack(side=RIGHT, padx=10)

        img_refresh = Image.open("imagenes/update.png")
        refresh_icon = CTkImage(dark_image=img_refresh, light_image=img_refresh, size=(30, 30))
        btn_refresh = CTkButton(frame_superior, text=" Actualizar",
                                 fg_color="transparent", command=self.actualizar_historial,
                                 image=refresh_icon, hover_color="#00501B", text_color=("black", "white"),
                                 font=("Ubuntu", 18, "bold"))
        btn_refresh.pack(side=RIGHT, padx=10)

        # Main Content Area
        self.frame_contenido_principal = CTkFrame(self, fg_color='white')
        self.frame_contenido_principal.pack(expand=True, fill=BOTH, padx=30, pady=20)

        self.tree_frame = CTkFrame(self.frame_contenido_principal, corner_radius=20)
        self.tree_frame.pack(pady=20, expand=True, fill=BOTH)

        tree_scroll = Scrollbar(self.tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#d5ffff", foreground="black", rowheight=25, fieldbackground="#FCFCFC")
        style.map('Treeview', background=[('selected', "#008fa8")])

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=tree_scroll.set,
                                    selectmode="extended", show="headings")
        self.my_tree.pack(expand=True, fill=BOTH)
        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("Fecha", "Placa", "Marca", "Modelo")
        for col in self.my_tree['columns']:
            self.my_tree.column(col, anchor=CENTER, width=150)
            self.my_tree.heading(col, text=col, anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#00A86B")

    def actualizar_historial(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        try:
            self.mydb.commit()
            self.my_cursor.execute("""
                SELECT DATE_FORMAT(h.Fecha_Eliminacion, '%Y-%m-%d') as FechaEliminado, v.Placa, m.Nombre, o.Nombre
                FROM historial_alquileres h
                INNER JOIN vehiculo v ON h.Placa_Vehiculo = v.Placa
                INNER JOIN marca m ON v.ID_Marca = m.ID
                INNER JOIN modelo o ON v.ID_Modelo = o.ID
                ORDER BY h.Fecha_Eliminacion DESC
            """)
            records = self.my_cursor.fetchall()
            
            for i, record in enumerate(records):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.my_tree.insert('', 'end', iid=i, values=record, tags=(tag,))
        except Exception as e:
            print(f"Error updating history frame: {e}")

