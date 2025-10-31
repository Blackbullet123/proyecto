from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image

class FrameDatosDetallados(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='white')
        self.controlador = controlador

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="control_alquiler_Reych"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID;")
        rows = cursor.fetchall()


        conn.commit()
        conn.close()


        style = ttk.Style()

        style.theme_use('clam')

        style.configure(
            "Treeview",
            background="#5dc1b9",
            foreground="black",
            rowheight=25,
            fieldbackground="#FCFCFC"
        )

        style.map('Treeview',
                background=[('selected',"#005954")])

        self.tree_frame_detallado = Frame(self)
        self.tree_frame_detallado.pack(pady=0, expand=True, fill=BOTH)

        tree_scroll = Scrollbar(self.tree_frame_detallado)
        tree_scroll.pack(side=RIGHT,fill=Y)

        bara = Scrollbar(self.tree_frame_detallado, orient=HORIZONTAL)
        bara.pack(side=BOTTOM,fill=X)

        my_tree = ttk.Treeview(self.tree_frame_detallado, yscrollcommand=tree_scroll.set, xscrollcommand=bara.set, selectmode="extended",show="headings")
        my_tree.pack(fill=Y, expand=Y)

        tree_scroll.config(command=my_tree.yview)
        bara.config(command=my_tree.xview)

        #CREACION DE COLUMNAS
        my_tree['columns']=("COD","RIF","Nombre","TLF","Direccion","CI","Nombre_r","Apellido","Placa","Color","Año","Marca","Modelo")

        my_tree.column("COD",anchor=CENTER,width=85)
        my_tree.column("RIF",anchor=CENTER,width=85)
        my_tree.column("Nombre",anchor=CENTER,width=85)
        my_tree.column("TLF",anchor=CENTER,width=140)
        my_tree.column("Direccion",anchor=CENTER,width=140)
        my_tree.column("CI",anchor=CENTER,width=140)
        my_tree.column("Nombre_r",anchor=CENTER,width=140)
        my_tree.column("Apellido",anchor=CENTER,width=140)
        my_tree.column("Placa",anchor=CENTER,width=140)
        my_tree.column("Color",anchor=CENTER,width=140)
        my_tree.column("Año",anchor=CENTER,width=140)
        my_tree.column("Marca",anchor=CENTER,width=140)
        my_tree.column("Modelo",anchor=CENTER,width=140)

        my_tree.heading("COD", text="Cod.",anchor=CENTER)
        my_tree.heading("RIF", text="RIF.",anchor=CENTER)
        my_tree.heading("Nombre", text="Empresa",anchor=CENTER)
        my_tree.heading("TLF", text="Teléfono",anchor=CENTER)
        my_tree.heading("Direccion", text="Direccion",anchor=CENTER)
        my_tree.heading("CI", text="C.I",anchor=CENTER)
        my_tree.heading("Nombre_r", text="Representante ",anchor=CENTER)
        my_tree.heading("Apellido", text="Apellido",anchor=CENTER)
        my_tree.heading("Placa", text=" Placa",anchor=CENTER)
        my_tree.heading("Color", text="Color",anchor=CENTER)
        my_tree.heading("Año", text="Año",anchor=CENTER)
        my_tree.heading("Marca", text="Marca",anchor=CENTER)
        my_tree.heading("Modelo", text="Modelo",anchor=CENTER)

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#5dc1b9")

        
        count = 0
        for row in rows:
            if count % 2 == 0:
                my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('evenrow',))#,
            else:
                my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('oddrow',))
            count += 1

        my_tree.pack()
