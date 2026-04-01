from tkinter import *
import tkinter as tk
import io
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image as RLImage, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.lib import colors
from datetime import datetime
import mysql.connector
import pandas as pd
import warnings
import numpy as np
from forms.vista_previa import vista_previa_3,vista_previa_2,vista_previa_grafica, vista_previa_historial, vista_previa_mantenimiento

warnings.filterwarnings("ignore", category=UserWarning, message=".*pandas only supports SQLAlchemy.*")

def imprimir_grafica(usuario_tipo="Desconocido"):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="control_alquiler_Reych"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM alquiler")
    total_alquileres = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM alquiler WHERE MONTH(Fecha) = MONTH(CURRENT_DATE()) AND YEAR(Fecha) = YEAR(CURRENT_DATE())")
    mes_actual = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT m.Nombre FROM alquiler a JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa 
        JOIN marca m ON v.ID_Marca = m.ID GROUP BY m.Nombre ORDER BY COUNT(*) DESC LIMIT 1
    """)
    res = cursor.fetchone()
    marca_preferida = res[0] if res else "N/A"

    cursor.execute("""
        SELECT m.Nombre, COUNT(a.COD_Alquiler)
        FROM alquiler a
        INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa
        INNER JOIN marca m ON v.ID_Marca = m.ID
        GROUP BY m.Nombre
        ORDER BY COUNT(a.COD_Alquiler) DESC
    """)
    datos_marcas = cursor.fetchall()
    
    cursor.execute("""
        SELECT DATE_FORMAT(Fecha, '%Y-%m') as Mes, COUNT(*) as Total
        FROM alquiler GROUP BY Mes ORDER BY Mes ASC LIMIT 12
    """)
    datos_mensual = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if not datos_marcas and not datos_mensual:
        print("No hay datos para generar el reporte")
        return

    marcas = [d[0] for d in datos_marcas]
    cantidades_marcas = [d[1] for d in datos_marcas]
    
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(marcas, cantidades_marcas, color="#00501B")
    ax1.set_title("Vehículos más Alquilados", fontweight="bold")
    ax1.set_ylabel("Cantidad")
    ax1.set_facecolor("#EEEEEE")
    fig1.patch.set_facecolor("#EEEEEE")
    
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='PNG', bbox_inches='tight')
    buf1.seek(0)
    plt.close(fig1)
    
    img_marcas = RLImage(buf1, width=420, height=210)

    meses_m = [d[0] for d in datos_mensual]
    cantidades_m = [d[1] for d in datos_mensual]
    total_anual = sum(cantidades_m) if cantidades_m else 1
    colores_palette = ["#4DB6AC", "#2E7D32", "#8BC34A", "#795548", "#00838F"]
    
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    ax2.set_facecolor("#EEEEEE")
    fig2.patch.set_facecolor("#EEEEEE")
    
    y_pos = np.arange(len(meses_m))
    bar_height = 0.6
    
    ax2.barh(y_pos, [100]*len(meses_m), height=bar_height, color="#D0D0D0", alpha=0.3)
    
    porcentajes = [(c / total_anual * 100) if total_anual > 0 else 0 for c in cantidades_m]

    for i, (p, c) in enumerate(zip(porcentajes, cantidades_m)):
        color = colores_palette[i % len(colores_palette)]
        ax2.barh(y_pos[i], p, height=bar_height, color=color)
        
        ax2.text(p - 1.5 if p > 8 else p + 1.5, y_pos[i], f"{int(p)}%", 
                va='center', ha='right' if p > 8 else 'left', 
                color='white' if p > 8 else 'black', fontsize=9, fontweight='bold')
        
        ax2.text(103, y_pos[i], meses_m[i], va='center', ha='left', color='black', fontsize=9)

    ax2.set_title("Inforgrafía: Alquileres Mensuales (% Anual)", fontweight="bold", fontsize=12, pad=15)
    ax2.set_xlim(0, 125)
    ax2.set_yticks([])
    ax2.axis('off')
    
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='PNG', bbox_inches='tight', facecolor=fig2.get_facecolor())
    buf2.seek(0)
    plt.close(fig2)
    
    img_mensual = RLImage(buf2, width=440, height=220)

    doc = SimpleDocTemplate("PDF/Grafica.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    def fecha_pdf():
        ahora = datetime.now()
        return ahora.strftime("%d/%m/%Y %I:%M %p")

    datos_kpi = [
        [Paragraph("<para align=center><b>TOTAL ALQUILERES</b></para>", styles['Normal']), 
         Paragraph("<para align=center><b>ALQUILERES ESTE MES</b></para>", styles['Normal']), 
         Paragraph("<para align=center><b>MARCA PREFERIDA</b></para>", styles['Normal'])],
        [Paragraph(f"<para align=center><font size=15><b>{total_alquileres}</b></font></para>", styles['Normal']),
         Paragraph(f"<para align=center><font size=15><b>{mes_actual}</b></font></para>", styles['Normal']),
         Paragraph(f"<para align=center><font size=15><b>{marca_preferida}</b></font></para>", styles['Normal'])]
    ]
    
    tabla_kpi = Table(datos_kpi, colWidths=[180, 180, 180])
    tabla_kpi.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.seagreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    p_label0 = Paragraph("<b>    <br/></b>")
    p_label3 = Paragraph("<b>RIF:</b> J-080204204")
    p_label4 = Paragraph("<b>Telefono:</b> 02832550911")
    p_label_user = Paragraph(f"<b>Generado por:</b> {usuario_tipo}")
    p_label9 = Paragraph(f"<b>Fecha:</b> {fecha_pdf()}")
    p_label10 = Paragraph("<b>    <br/></b>")

    p_title = Paragraph("<b>Reporte Estadístico de Alquileres</b>", title_style)

    imagen_path = "imagenes/membrete.jpg"
    imagen = RLImage(imagen_path, width=570, height=70)

    imagen_2 = "imagenes/Reych_imp.png"
    imagen_alq = RLImage(imagen_2, width=130, height=110)

    def add_image(canvas, doc):
        imagen_alq.drawOn(canvas, 450, 610)
        imagen.drawOn(canvas, 20, 715)

    tabla_img_mensual = Table([[img_mensual]], colWidths=[540])
    tabla_img_mensual.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    
    tabla_img_marcas = Table([[img_marcas]], colWidths=[540])
    tabla_img_marcas.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))

    elements = [
        p_label0, p_label3, p_label4, p_label_user, p_label9, p_label10,
        Spacer(1, 20),
        p_title, 
        Spacer(1, 15),
        tabla_kpi,
        Spacer(1, 25),
        tabla_img_mensual,
        Spacer(1, 15),
        tabla_img_marcas
    ]

    doc.build(elements, onFirstPage=add_image)
    vista_previa_grafica()
        
        
def imprimir_todos(usuario_tipo="Desconocido"):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='control_alquiler_Reych'
        )

        query = ("SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.Nombre AS Empresa, c.telefono, c.direccion, r.CI, r.nombre AS R_Nombre, r.apellido AS R_Apellido, v.Placa, v.Color, v.Año, m.Nombre AS Marca, o.Nombre AS Modelo FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID ORDER BY a.COD_Alquiler ASC;")
        df = pd.read_sql(query, conn)
        
        hoy = datetime.now().date()
        def calculate_status(row):
            exp_date = row['Fecha_Expiracion']
            try:
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                elif isinstance(exp_date, (datetime, pd.Timestamp)):
                    exp_date = exp_date.date()
                
                return "● Finalizado" if exp_date < hoy else "● Activo"
            except:
                return "● Desconocido"

        df['Estado'] = df.apply(calculate_status, axis=1)
        
        cols = ['Estado', 'COD_Alquiler', 'Fecha', 'RIF', 'Empresa', 'telefono', 'direccion', 'CI', 'R_Nombre', 'R_Apellido', 'Placa', 'Color', 'Año', 'Marca', 'Modelo']
        df = df[cols]
        
        df.columns = ['Estado', 'COD', 'Fecha Inicial', 'RIF', 'Empresa', 'Teléfono', 'Dirección', 'C.I', 'R. Nombre', 'R. Apellido', 'Placa', 'Color', 'Año', 'Marca', 'Modelo']

        doc = SimpleDocTemplate("PDF/Todos los alquilados.pdf", pagesize=landscape(letter), leftMargin=30, rightMargin=30)
        data = [df.columns.tolist()] + df.values.tolist()
        
        def fecha_pdf():
            ahora = datetime.now()
            return ahora.strftime("%d/%m/%Y %I:%M %p")

        label0 = "<b>    <br/></b>"
        label3 = "<b>RIF:</b> J-080204204"
        label4 = "<b>Telefono:</b> 02832550911"
        label_user = f"<b>Generado por:</b> {usuario_tipo}"
        label9 = f"<b>Fecha:</b> {fecha_pdf()}"
        label10 = "<b>    <br/></b>"

        p_label0 = Paragraph(label0)
        p_label3 = Paragraph(label3)
        p_label4 = Paragraph(label4)
        p_label_user = Paragraph(label_user)
        p_label9 = Paragraph(label9)
        p_label10 = Paragraph(label10)

        styles = getSampleStyleSheet()
        title = "<b>Todo los Vehiculos Alquilados</b>"
        p_title = Paragraph(title, styles['Title'])
        
        
        imagen_path = "imagenes/membrete.jpg"
        imagen = RLImage(imagen_path, width=750, height=70) 
        
        pdx = 20
        pdy = 520 
        
        imagen_2 = "imagenes/Reych_imp.png"
        imagen_alq = RLImage(imagen_2, width=130, height=110)
        
        x = 650 
        y = 420


        def add_image(canvas, doc):
            imagen_alq.drawOn(canvas, x, y)
            imagen.drawOn(canvas, pdx, pdy)
            

        table = Table(data)
        
        style_list = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 0), (-1, -1), 6.5), # Un poco más grande ahora que estamos en Landscape
        ]
        
        for i, row in enumerate(data[1:], start=1):
            if "Activo" in row[0]:
                style_list.append(('BACKGROUND', (0, i), (0, i), colors.seagreen))
                style_list.append(('TEXTCOLOR', (0, i), (0, i), colors.whitesmoke))
            elif "Finalizado" in row[0]:
                style_list.append(('BACKGROUND', (0, i), (0, i), colors.red))
                style_list.append(('TEXTCOLOR', (0, i), (0, i), colors.whitesmoke))
        
        table.setStyle(TableStyle(style_list))

        elements = [p_label0, p_label3, p_label4, p_label_user, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements, onFirstPage=add_image)
        conn.close()
        vista_previa_3()
    
def imprimir_vehiculos(usuario_tipo="Desconocido"):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='control_alquiler_Reych'
        )

        query = ("SELECT v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID WHERE a.COD_Alquiler IS NULL ORDER BY v.Placa;")
        df = pd.read_sql(query, conn)
        
        doc = SimpleDocTemplate("PDF/Vehiculos.pdf", pagesize=letter)
        data = [df.columns[:,].tolist()] + df.values.tolist()
        
        def fecha_pdf_2():
            ahora = datetime.now()
            return ahora.strftime("%d/%m/%Y %I:%M %p")

        label0 = "<b>    <br/></b>"
        label3 = "<b>RIF:</b> J-080204204"
        label4 = "<b>Telefono:</b> 02832550911"
        label_user = f"<b>Generado por:</b> {usuario_tipo}"
        label9 = f"<b>Fecha:</b> {fecha_pdf_2()}"
        label10 = "<b>    <br/></b>"

        p_label0 = Paragraph(label0)
        p_label3 = Paragraph(label3)
        p_label4 = Paragraph(label4)
        p_label_user = Paragraph(label_user)
        p_label9 = Paragraph(label9)
        p_label10 = Paragraph(label10)

        styles = getSampleStyleSheet()
        title = "<b>Vehiculos Disponibles</b>"
        p_title = Paragraph(title, styles['Title'])
        
        
        imagen_path = "imagenes/membrete.jpg"
        imagen = RLImage(imagen_path, width=570, height=70)
        
        pdx = 20
        pdy = 715
        
        imagen_2 = "imagenes/Reych_imp.png"
        imagen_alq = RLImage(imagen_2, width=130, height=110)
        
        x = 450
        y = 610

        def add_image(canvas, doc):
            imagen_alq.drawOn(canvas, x, y)
            imagen.drawOn(canvas, pdx, pdy)
            



        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ])
        table.setStyle(style)

        elements = [p_label0, p_label3, p_label4, p_label_user, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements, onFirstPage=add_image)
        conn.close()
        vista_previa_2()

def imprimir_historial(usuario_tipo="Desconocido"):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='control_alquiler_Reych'
    )

    query = ("""
        SELECT DATE_FORMAT(h.Fecha_Eliminacion, '%Y-%m-%d') as FechaEliminado, v.Placa, m.Nombre, o.Nombre
        FROM historial_alquileres h
        INNER JOIN vehiculo v ON h.Placa_Vehiculo = v.Placa
        INNER JOIN marca m ON v.ID_Marca = m.ID
        INNER JOIN modelo o ON v.ID_Modelo = o.ID
        ORDER BY h.Fecha_Eliminacion DESC
    """)
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(records, columns=["Fecha Eliminado", "Placa", "Marca", "Modelo"])
    
    doc = SimpleDocTemplate("PDF/Historial_Eliminados.pdf", pagesize=letter)
    data = [df.columns[:,].tolist()] + df.values.tolist()
    
    def fecha_pdf():
        ahora = datetime.now()
        return ahora.strftime("%d/%m/%Y %I:%M %p")

    label0 = "<b>    <br/></b>"
    label3 = "<b>RIF:</b> J-080204204"
    label4 = "<b>Telefono:</b> 02832550911"
    label_user = f"<b>Generado por:</b> {usuario_tipo}"
    label9 = f"<b>Fecha:</b> {fecha_pdf()}"
    label10 = "<b>    <br/></b>"

    p_label0 = Paragraph(label0)
    p_label3 = Paragraph(label3)
    p_label4 = Paragraph(label4)
    p_label_user = Paragraph(label_user)
    p_label9 = Paragraph(label9)
    p_label10 = Paragraph(label10)

    styles = getSampleStyleSheet()
    title = "<b>Reporte Historial Vehículos Eliminados</b>"
    p_title = Paragraph(title, styles['Title'])
    
    imagen_path = "imagenes/membrete.jpg"
    imagen = RLImage(imagen_path, width=570, height=70)
    pdx = 20
    pdy = 715
    imagen_2 = "imagenes/Reych_imp.png"
    imagen_alq = RLImage(imagen_2, width=130, height=110)
    x = 450
    y = 610

    def add_image(canvas, doc):
        imagen_alq.drawOn(canvas, x, y)
        imagen.drawOn(canvas, pdx, pdy)


    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ])
    table.setStyle(style)

    elements = [p_label0, p_label3, p_label4, p_label_user, p_label9, p_label10, p_title, Spacer(1, 20), table]
    
    doc.build(elements, onFirstPage=add_image)
    vista_previa_historial()

def imprimir_mantenimiento(usuario_tipo="Desconocido"):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='control_alquiler_Reych'
    )
    cursor = conn.cursor()

    query = """
        SELECT v.Placa, m.Nombre AS Marca, o.Nombre AS Modelo, v.dias_mantenimiento,
               (SELECT MAX(Fecha) FROM mantenimiento WHERE Placa = v.Placa) AS UltimaFecha
        FROM vehiculo v
        INNER JOIN marca m ON v.ID_Marca = m.ID
        INNER JOIN modelo o ON v.ID_Modelo = o.ID
    """
    cursor.execute(query)
    vehiculos = cursor.fetchall()
    conn.close()

    necesario = []
    sin_registro = []
    al_dia = []

    hoy = datetime.now().date()

    for placa, marca, modelo, dias_mantenimiento, ultima_fecha in vehiculos:
        row = [placa, marca, modelo, dias_mantenimiento, str(ultima_fecha) if ultima_fecha else "N/A"]
        
        if not ultima_fecha:
            sin_registro.append(row)
        else:
            dias_pasados = (hoy - ultima_fecha).days
            dias_restantes = dias_mantenimiento - dias_pasados
            if dias_restantes <= 1:
                necesario.append(row)
            else:
                al_dia.append(row)

    doc = SimpleDocTemplate("PDF/Mantenimiento.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    def fecha_pdf():
        return datetime.now().strftime("%d/%m/%Y %I:%M %p")

    elements = []
    
    elements.extend([
        Paragraph("<b>    <br/></b>"),
        Paragraph("<b>RIF:</b> J-080204204"),
        Paragraph("<b>Telefono:</b> 02832550911"),
        Paragraph(f"<b>Generado por:</b> {usuario_tipo}"),
        Paragraph(f"<b>Fecha:</b> {fecha_pdf()}"),
        Paragraph("<b>    <br/></b>"),
        Paragraph("<b>Reporte de Mantenimiento de Vehículos</b>", styles['Title']),
        Spacer(1, 20)
    ])

    def crear_seccion(titulo, datos, color_fondo):
        if not datos:
            return []
        
        elements_sec = [
            Paragraph(f"<b>{titulo}</b>", styles['Heading2']),
            Spacer(1, 10)
        ]
        
        headers = ["Placa", "Marca", "Modelo", "Frecuencia (Días)", "Último Mantenimiento"]
        table_data = [headers] + datos
        
        table = Table(table_data, colWidths=[80, 100, 100, 100, 120])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), color_fondo),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ])
        table.setStyle(style)
        elements_sec.append(table)
        elements_sec.append(Spacer(1, 20))
        return elements_sec

    elements.extend(crear_seccion("MANTENIMIENTO NECESARIO", necesario, colors.red))
    elements.extend(crear_seccion("SIN REGISTRO DE MANTENIMIENTO", sin_registro, colors.dodgerblue))
    elements.extend(crear_seccion("ÓPTIMAS CONDICIONES", al_dia, colors.seagreen))

    imagen_path = "imagenes/membrete.jpg"
    imagen = RLImage(imagen_path, width=570, height=70)
    imagen_2 = "imagenes/Reych_imp.png"
    imagen_alq = RLImage(imagen_2, width=130, height=110)

    def add_image(canvas, doc):
        imagen_alq.drawOn(canvas, 450, 610)
        imagen.drawOn(canvas, 20, 715)

    doc.build(elements, onFirstPage=add_image)
    vista_previa_mantenimiento()
