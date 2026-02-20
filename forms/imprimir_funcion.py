from tkinter import *
import tkinter as tk
import io
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.lib import colors
from datetime import datetime
import mysql.connector
import pandas as pd
from forms.vista_previa import vista_previa_3,vista_previa_2,vista_previa_grafica

def imprimir_grafica():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="control_alquiler_Reych"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.Nombre, COUNT(a.COD_Alquiler)
        FROM alquiler a
        INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa
        INNER JOIN marca m ON v.ID_Marca = m.ID
        GROUP BY m.Nombre
        ORDER BY COUNT(a.COD_Alquiler) DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    if not datos:
        print("No hay datos para generar la gráfica")
        return

    marcas = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(marcas, cantidades, color="#00501B")
    ax.set_xlabel("Marca")
    ax.set_ylabel("Total")
    ax.set_facecolor("#EEEEEE")
    fig.patch.set_facecolor("#EEEEEE")

    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    grafica_pdf = Image(buf, width=400, height=300)

    doc = SimpleDocTemplate("PDF/Grafica.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']

    def fecha_pdf():
        ahora = datetime.now()
        return ahora.strftime("%d/%m/%Y %I:%M %p")

    p_label0 = Paragraph("<b>    <br/></b>")
    p_label3 = Paragraph("<b>RIF:</b> J-080204204")
    p_label4 = Paragraph("<b>Telefono:</b> 02832550911")
    p_label9 = Paragraph(f"<b>Fecha:</b> {fecha_pdf()}")
    p_label10 = Paragraph("<b>    <br/></b>")

    p_title = Paragraph("<b>Reporte de Alquileres por Marca</b>", title_style)

    imagen_path = "imagenes/membrete.jpg"
    imagen = Image(imagen_path, width=570, height=70)

    imagen_2 = "imagenes/Reych_imp.png"
    imagen_alq = Image(imagen_2, width=130, height=110)

    def add_image(canvas, doc):
        imagen_alq.drawOn(canvas, 450, 610)
        imagen.drawOn(canvas, 20, 715)

    elements = [
        p_label0, p_label3, p_label4, p_label9, p_label10,
        p_title, Spacer(1, 20), grafica_pdf
    ]

    doc.build(elements, onFirstPage=add_image)

    vista_previa_grafica()
        
        
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
        
        def fecha_pdf():
            ahora = datetime.now()
            return ahora.strftime("%d/%m/%Y %I:%M %p")

        # Crear los textos que funcionarán como etiquetas
        label0 = "<b>    <br/></b>"
        label3 = "<b>RIF:</b> J-080204204"
        label4 = "<b>Telefono:</b> 02832550911"
        label9 = f"<b>Fecha:</b> {fecha_pdf()}"
        label10 = "<b>    <br/></b>"

        # Crear los párrafos con los textos
        p_label0 = Paragraph(label0)
        p_label3 = Paragraph(label3)
        p_label4 = Paragraph(label4)
        p_label9 = Paragraph(label9)
        p_label10 = Paragraph(label10)

        styles = getSampleStyleSheet()
        title = "<b>Todo los Vehiculos Alquilados</b>"
        p_title = Paragraph(title, styles['Title'])
        
        
        imagen_path = "imagenes/membrete.jpg"
        imagen = Image(imagen_path, width=570, height=70)
        
        pdx = 20
        pdy = 715
        
        imagen_2 = "imagenes/Reych_imp.png"
        imagen_alq = Image(imagen_2, width=130, height=110)
        
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
        query = ("SELECT v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca ORDER BY v.Placa;")
        df = pd.read_sql(query, conn)
        
        # Crear el PDF
        doc = SimpleDocTemplate("PDF/Vehiculos.pdf", pagesize=letter)
        data = [df.columns[:,].tolist()] + df.values.tolist()
        
        def fecha_pdf_2():
            ahora = datetime.now()
            return ahora.strftime("%d/%m/%Y %I:%M %p")

        # Crear los textos que funcionarán como etiquetas
        label0 = "<b>    <br/></b>"
        label3 = "<b>RIF:</b> J-080204204"
        label4 = "<b>Telefono:</b> 02832550911"
        label9 = f"<b>Fecha:</b> {fecha_pdf_2()}"
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
        
        imagen_2 = "imagenes/Reych_imp.png"
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