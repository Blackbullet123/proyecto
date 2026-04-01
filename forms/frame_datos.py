from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
from PIL import Image as PILImage, ImageDraw, ImageFont
from datetime import datetime
import mysql.connector
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image as RLImage, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from forms.vista_previa import vista_previa_1
import pandas as pd
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class FrameDatosDetallados(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=("#FFFFFF", "#1A1A1A"))

        self.controlador = controlador
        
        def get_text_icon(texto, color_f):
            try:
                font = ImageFont.truetype("arialbd.ttf", 13)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 13)
                except:
                    font = ImageFont.load_default()
            
            temp_img = PILImage.new('RGBA', (120, 30))
            draw = ImageDraw.Draw(temp_img)
            bbox = draw.textbbox((0, 0), texto, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            icon_img = PILImage.new('RGBA', (w + 10, h + 5), (255, 255, 255, 0))
            d = ImageDraw.Draw(icon_img)
            d.text((5, 2), texto, fill=color_f, font=font)
            return icon_img

        self.tk_act_text = ImageTk.PhotoImage(get_text_icon("● Activo", "#2E7D32"))
        self.tk_fin_text = ImageTk.PhotoImage(get_text_icon("● Finalizado", "#D32F2F"))
        self.tk_desc_text = ImageTk.PhotoImage(PILImage.new('RGBA', (1, 1), (0,0,0,0))) 

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="control_alquiler_Reych"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color, v.Año, m.Nombre, o.Nombre, a.Fecha_Expiracion FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID;")
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
        
        self.tree_frame_detallado = CTkFrame(self, fg_color=("#FFFFFF", "#1A1A1A"))
        self.tree_frame_detallado.pack(pady=0, expand=True, fill=BOTH)

        tree_scroll = Scrollbar(self.tree_frame_detallado)
        tree_scroll.pack(side=RIGHT,fill=Y)

        bara = Scrollbar(self.tree_frame_detallado, orient=HORIZONTAL)
        bara.pack(side=BOTTOM,fill=X)

        self.my_tree = ttk.Treeview(self.tree_frame_detallado, yscrollcommand=tree_scroll.set, xscrollcommand=bara.set, selectmode="extended",show="tree headings")
        self.my_tree.tag_configure('oddrow', background="white", foreground="black")
        self.my_tree.tag_configure('evenrow', background="#00A86B", foreground="black")
        self.my_tree.tag_configure('activo', foreground="black") 
        self.my_tree.tag_configure('finalizado', foreground="black") 

        self.my_tree.pack(fill=Y, expand=Y)

        tree_scroll.config(command=self.my_tree.yview)
        bara.config(command=self.my_tree.xview)

        #CREACION DE COLUMNAS
        self.my_tree['columns']=("COD","RIF","Nombre","TLF","Direccion","CI","Nombre_r","Apellido","Placa","Color","Año","Marca","Modelo")

        self.my_tree.column("#0",anchor=CENTER,width=90)

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

        self.my_tree.heading("#0", text="Estado", anchor=CENTER)

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


        
        hoy = datetime.now().date()
        count = 0
        for row in rows:
            try:
                exp_date = row[13]
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                elif isinstance(exp_date, datetime):
                    exp_date = exp_date.date()
                
                if exp_date < hoy:
                    img_icon = self.tk_fin_text
                    tag_status = 'finalizado'
                else:
                    img_icon = self.tk_act_text
                    tag_status = 'activo'
            except:
                img_icon = self.tk_desc_text
                tag_status = ''

            tag = ('evenrow' if count % 2 == 0 else 'oddrow', tag_status)
            self.my_tree.insert(parent='',index='end',text='',values=row[:15],tags=tag, image=img_icon)
            count += 1

        self.my_tree.pack()

    def imprimir_fila_seleccionada(self, usuario_tipo="Desconocido", parent=None):
        selected_item = self.my_tree.selection()
        if not selected_item:
            messagebox.showerror("ERROR", "No se ha seleccionado una fila", parent=parent)
            return

        for item in selected_item:
            values = list(self.my_tree.item(item, "values"))
            
            try:
                exp_date = values[2] 
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                
                hoy = datetime.now().date()
                if exp_date < hoy:
                    status_text = "● Finalizado"
                    status_bg = colors.red
                else:
                    status_text = "● Activo"
                    status_bg = colors.seagreen
            except:
                status_text = "● Desconocido"
                status_bg = colors.grey
            
            values.insert(0, status_text)
        
        doc = SimpleDocTemplate("PDF/datos de vehiculos detallado.pdf", pagesize=landscape(letter), leftMargin=30, rightMargin=30)
        elements = []
        
        data = [
            ['Estado', 'COD', 'F. Inicial', 'F. Final', 'RIF', 'Empresa', 'Teléfono', 'Dirección', 'C.I', 'R. Nombre', 'R. Apellido', 'Placa', 'Color', 'Año', 'Marca', 'Modelo'],
            values
        ]
        
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
        title = "<b>Datos Detallados</b>"
        p_title = Paragraph(title, styles['Title'])
        
        imagen_path = "imagenes/membrete.jpg"
        imagen = RLImage(imagen_path, width=750, height=70)
        
        pdx = 20
        pdy = 520 
        
        imagen_2 = "imagenes/Reych.png"
        imagen_alq = RLImage(imagen_2, width=130, height=110)
        
        x = 650 
        y = 420

        def add_image(canvas, doc):
            imagen_alq.drawOn(canvas, x, y)
            imagen.drawOn(canvas, pdx, pdy)
        data = [
            ['Estado', 'COD', 'RIF', 'Empresa', 'Teléfono', 'Dirección', 'C.I', 'R. Nombre', 'R. Apellido', 'Placa', 'Color', 'Año', 'Marca', 'Modelo'],
            values
        ]
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('BACKGROUND', (0, 1), (0, 1), status_bg),
                            ('TEXTCOLOR', (0, 1), (0, 1), colors.whitesmoke),
                            ('FONTSIZE', (0, 0), (-1, -1), 6.5),
                            ])
        table.setStyle(style)
        elements = [p_label0, p_label3, p_label4, p_label_user, p_label9, p_label10, p_title, Spacer(1, 20), table]
        
        doc.build(elements, onFirstPage=add_image)
        vista_previa_1()
    
    def buscar(self, searched):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123456",
            port = "3306",
            database = "control_alquiler_Reych"
        )
        my_cursor = mydb.cursor()

        sql_base = "SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color, v.Año, m.Nombre, o.Nombre, a.Fecha_Expiracion FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID "

        if not searched.strip():
            sql = sql_base + " ORDER BY a.COD_Alquiler ASC;"
            my_cursor.execute(sql)
        elif searched.isdigit():
            sql = sql_base + " WHERE a.COD_Alquiler = %s ORDER BY a.COD_Alquiler ASC;"
            my_cursor.execute(sql, (searched,))
        else:
            like_pattern = f"%{searched}%"
            sql = sql_base + """ WHERE (CAST(a.COD_Alquiler AS CHAR) LIKE %s 
                                 OR c.RIF LIKE %s 
                                 OR c.Nombre LIKE %s 
                                 OR c.telefono LIKE %s 
                                 OR r.CI LIKE %s 
                                 OR v.Placa LIKE %s
                                 OR m.Nombre LIKE %s 
                                 OR o.Nombre LIKE %s) 
                                 ORDER BY a.COD_Alquiler ASC;"""
            my_cursor.execute(sql, (like_pattern, like_pattern, like_pattern, like_pattern, like_pattern, like_pattern, like_pattern, like_pattern))

        items = my_cursor.fetchall()
        hoy = datetime.now().date()
        count = 0
        for item in items:
            try:
                exp_date = item[13]
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                elif isinstance(exp_date, datetime):
                    exp_date = exp_date.date()
                
                if exp_date < hoy:
                    img_icon = self.tk_fin_text
                    tag_status = 'finalizado'
                else:
                    img_icon = self.tk_act_text
                    tag_status = 'activo'
            except:
                img_icon = self.tk_desc_text
                tag_status = ''

            tag = ('evenrow' if count % 2 == 0 else 'oddrow', tag_status)
            self.my_tree.insert(parent='',index='end',text='',values=item[:13],tags=tag, image=img_icon)
            count += 1
        mydb.close()
    
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

        my_cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre, a.Fecha_Expiracion FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID ORDER BY a.COD_Alquiler ASC;")
        items = my_cursor.fetchall()

        hoy = datetime.now().date()
        count = 0
        for item in items:
            try:
                exp_date = item[13]
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                elif isinstance(exp_date, datetime):
                    exp_date = exp_date.date()
                
                if exp_date < hoy:
                    img_icon = self.tk_fin_text
                    tag_status = 'finalizado'
                else:
                    img_icon = self.tk_act_text
                    tag_status = 'activo'
            except:
                img_icon = self.tk_desc_text
                tag_status = ''

            tag = ('evenrow' if count % 2 == 0 else 'oddrow', tag_status)
            self.my_tree.insert(parent='',index='end',text='',values=item[:13],tags=tag, image=img_icon)
            count += 1

        conn.close()