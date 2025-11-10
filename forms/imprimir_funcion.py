from tkinter import *
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import mysql.connector
import pandas as pd
from forms.vista_previa import vista_previa_3,vista_previa_2
        
        
def imprimir_todos():
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='control_alquiler_Reych'
        )

        # Consulta a la base de datos
        query = ("SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID;")
        df = pd.read_sql(query, conn)
        
        # Crear el PDF
        doc = SimpleDocTemplate("PDF/Todos los alquilados.pdf", pagesize=letter)
        data = [df.columns[:,].tolist()] + df.values.tolist()
        
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
        title = "<b>Todo los Vehiculos Alquilados</b>"
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
                            ('FONTSIZE', (0, 0), (-1, -1), 6.5),
                            ])
        table.setStyle(style)

        # Añadir las etiquetas al PDF
        elements = [p_label0, p_label3, p_label4, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements)
        vista_previa_3()
    
def imprimir_vehiculos():
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='control_alquiler_Reych'
        )

        # Consulta a la base de datos
        query = ("SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca ORDER BY a.COD_Alquiler ASC;")
        df = pd.read_sql(query, conn)
        
        # Crear el PDF
        doc = SimpleDocTemplate("PDF/Vehiculos.pdf", pagesize=letter)
        data = [df.columns[:,].tolist()] + df.values.tolist()
        
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
        title = "<b>Vehiculos Disponibles</b>"
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
                            ])
        table.setStyle(style)

        # Añadir las etiquetas al PDF
        elements = [p_label0, p_label3, p_label4, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements)
        vista_previa_2()