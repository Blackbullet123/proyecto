from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from reportlab.lib.pagesizes import letter
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from forms.vista_previa import vista_previa_1
import pandas as pd
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

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
        cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID;")
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

        self.my_tree = ttk.Treeview(self.tree_frame_detallado, yscrollcommand=tree_scroll.set, xscrollcommand=bara.set, selectmode="extended",show="headings")
        self.my_tree.pack(fill=Y, expand=Y)

        tree_scroll.config(command=self.my_tree.yview)
        bara.config(command=self.my_tree.xview)

        #CREACION DE COLUMNAS
        self.my_tree['columns']=("COD","RIF","Nombre","TLF","Direccion","CI","Nombre_r","Apellido","Placa","Color","Año","Marca","Modelo")

        self.my_tree.column("COD",anchor=CENTER,width=85)
        self.my_tree.column("RIF",anchor=CENTER,width=85)
        self.my_tree.column("Nombre",anchor=CENTER,width=85)
        self.my_tree.column("TLF",anchor=CENTER,width=120)
        self.my_tree.column("Direccion",anchor=CENTER,width=120)
        self.my_tree.column("CI",anchor=CENTER,width=120)
        self.my_tree.column("Nombre_r",anchor=CENTER,width=120)
        self.my_tree.column("Apellido",anchor=CENTER,width=120)
        self.my_tree.column("Placa",anchor=CENTER,width=120)
        self.my_tree.column("Color",anchor=CENTER,width=120)
        self.my_tree.column("Año",anchor=CENTER,width=120)
        self.my_tree.column("Marca",anchor=CENTER,width=120)
        self.my_tree.column("Modelo",anchor=CENTER,width=120)

        self.my_tree.heading("COD", text="Cod.",anchor=CENTER)
        self.my_tree.heading("RIF", text="RIF.",anchor=CENTER)
        self.my_tree.heading("Nombre", text="Empresa",anchor=CENTER)
        self.my_tree.heading("TLF", text="Teléfono",anchor=CENTER)
        self.my_tree.heading("Direccion", text="Direccion",anchor=CENTER)
        self.my_tree.heading("CI", text="Cedula",anchor=CENTER)
        self.my_tree.heading("Nombre_r", text="Representante ",anchor=CENTER)
        self.my_tree.heading("Apellido", text="Apellido",anchor=CENTER)
        self.my_tree.heading("Placa", text=" Placa",anchor=CENTER)
        self.my_tree.heading("Color", text="Color",anchor=CENTER)
        self.my_tree.heading("Año", text="Año",anchor=CENTER)
        self.my_tree.heading("Marca", text="Marca",anchor=CENTER)
        self.my_tree.heading("Modelo", text="Modelo",anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#00A86B")

        
        count = 0
        for row in rows:
            if count % 2 == 0:
                self.my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('evenrow',))#,
            else:
                self.my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('oddrow',))
            count += 1

        self.my_tree.pack()

    def imprimir_fila_seleccionada(self, parent=None):
        selected_item = self.my_tree.selection()
        if not selected_item:
            messagebox.showerror("ERROR", "No se ha seleccionado una fila", parent=parent)
            return

        for item in selected_item:
            values = self.my_tree.item(item, "values")
        
        doc = SimpleDocTemplate("PDF/datos de vehiculos detallado.pdf", pagesize=letter)
        elements = []
        
        data = [
            ['COD', 'RIF', 'Empresa', 'Teléfono', 'Direccion', 'C.I', 'Representante', 'Apellido', 'Placa', 'Color', 'Año', 'Marca', 'Modelo'],
            values
        ]
        
        # Crear los textos que funcionarán como etiquetas
        label0 = "<b>    <br/></b>"
        label3 = "<b>RIF:</b> J-080204204"
        label4 = "<b>Telefono:</b> 02832550911"
        label9 = "<b>     <br/></b>"
        label10 = "<b>    <br/></b>"

        # Crear los párrafos con los textos
        p_label0 = Paragraph(label0)
        p_label3 = Paragraph(label3)
        p_label4 = Paragraph(label4)
        p_label9 = Paragraph(label9)
        p_label10 = Paragraph(label10)

        # Crear el membrete con un título de alquitech
        styles = getSampleStyleSheet()
        title = "<b>Datos Detallados</b>"
        p_title = Paragraph(title, styles['Title'])
        
        imagen_path = "imagenes/membrete.jpg"
        imagen = Image(imagen_path, width=570, height=70)
        
        # Definir las coordenadas x y y para posicionar la imagen en el PDF
        pdx = 20
        pdy = 715
        
        imagen_2 = "imagenes/Reych.png"
        imagen_alq = Image(imagen_2, width=130, height=110)
        
        # Definir las coordenadas x y y para posicionar la imagen en el PDF
        x = 450
        y = 610

        # Añadir la imagen al canvas en las coordenadas especificadas
        def add_image(canvas, doc):
            imagen_alq.drawOn(canvas, x, y)
            imagen.drawOn(canvas, pdx, pdy)
            

        # Construir el documento PDF y añadir la función add_image al canvas
        doc.build([imagen_alq, imagen], onFirstPage=add_image)

        # Crear la tabla en el PDF
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('FONTSIZE', (0, 0), (-1, -1), 7),
                            ])
        table.setStyle(style)

        # Añadir las etiquetas al PDF
        elements = [p_label0, p_label3, p_label4, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements)
        vista_previa_1()
    
    def actualizar_tree_datos(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

            mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123456",
            port = "3306",
            database = "control_alquiler_Reych"
        )

        conn = mydb

        my_cursor = mydb.cursor()

        my_cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID ORDER BY a.COD_Alquiler ASC;")
        items = my_cursor.fetchall()

        count = 0

        for item in items:
            if count % 2 == 0:
                self.my_tree.insert(parent='',index='end',text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12]),tags=('evenrow',))
            else: 
                self.my_tree.insert(parent='',index='end',text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12]),tags=('oddrow',))

            count += 1

        conn.commit()
        conn.close()