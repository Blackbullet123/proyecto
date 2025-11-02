from tkinter import *
from tkinter import ttk
import tkinter as tk
import mysql.connector
from customtkinter import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import mysql.connector
from forms.imprimir_funcion import imprimir_todos
from forms.vista_previa import vista_previa_1
from tkinter import messagebox
import pandas as pd
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()


def detallado():
    
    class dato:
        def __init__(self):
            self.root = tk.Toplevel()
            self.root.title('EXPORTAR')
            self.root.geometry("670x420")
            self.root.config(background='#EEEEEE')
            

            def imprimir_fila_seleccionada():
                selected_item = my_tree.selection()
                if not selected_item:
                    messagebox.showerror("ERROR", "No se ha seleccionado una fila")
                    return

                for item in selected_item:
                    values = my_tree.item(item, "values")
                
                doc_path = get_project_root() / "PDF" / "datos de vehiculos detallado.pdf"
                doc = SimpleDocTemplate(doc_path, pagesize=letter)
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
                
                imagen_path = get_project_root() / "imagenes" / "membrete.jpg"
                if not imagen_path.exists():
                    messagebox.showerror("Error", "La imagen no se encuentra en la ruta especificada.")
                    return
                imagen = Image(imagen_path, width=570, height=70)
                
                # Definir las coordenadas x y y para posicionar la imagen en el PDF
                pdx = 20
                pdy = 715
                
                imagen_2 = get_project_root() / "imagenes" / "logoapp.png"
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

            frame_form = Frame(self.root,bd=0,relief=SOLID,bg='#2ca880',height=50)
            frame_form.pack(side="top",expand=NO,fill=BOTH)

            frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='black')
            frame_form_top.pack(side="top",fill=Y)
            title = Label(frame_form_top,text="Datos Detallados",font=('BOLD',25),fg="#fcfcfc",bg='#2ca880',pady=5)#008259
            title.pack(expand=YES,fill=BOTH)
            
            
            frame_form_top2 = CTkFrame(frame_form,fg_color='#2ca880', corner_radius=0)
            frame_form_top2.pack(side="top",fill=Y)
            
            
            imprimir = CTkButton(frame_form_top2,text="Reporte Detallado", command=imprimir_fila_seleccionada,corner_radius=15, 
                                           text_color="white",width=100,height=40,cursor='hand2',
                                        fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20))
            imprimir.grid(row=0, column=0,pady=10, padx=40)
            
            imprimir_general = CTkButton(frame_form_top2,text="Reporte General", command=imprimir_todos,corner_radius=15, 
                                           text_color="white",width=100,height=40,cursor='hand2',
                                        fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20))
            imprimir_general.grid(row=0, column=2,pady=5, padx=40)
            
            title_1 = Label(frame_form_top2,text="Imprimir",font=('BOLD',25),fg="#fcfcfc",bg='#2ca880',pady=5)#008259
            title_1.grid(row=0, column=1,pady=10, padx=20)
                  
            ####################### BUSQUEDA ################################
            def search_now():
                
                for item in my_tree.get_children():
                    my_tree.delete(item)

                mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "123456",
                    port = "3306",
                    database = "control_alquiler_Reych"
                )
                my_cursor = mydb.cursor()
                conn = mydb
                sql = "SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre_r, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID WHERE COD_Alquiler = {0}"

                my_cursor.execute(sql.format(buscar.get()))
                records = my_cursor.fetchall()
                
                count = 0
                for record in records:
                    if count % 2 == 0:
                        my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12]),tags=('evenrow',))#,
                    else:
                        my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12]),tags=('oddrow',))
                    count += 1

                conn.commit()
                conn.close()
                
            def actualizar_tree_2():
                    for item in my_tree.get_children():
                        my_tree.delete(item)

                        mydb = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "123456",
                        port = "3306",
                        database = "control_alquiler_Reych"
                    )

                    conn = mydb

                    my_cursor = mydb.cursor()

                    my_cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.Nombre, c.telefono, c.direccion, r.CI, r.nombre_r, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID;")
                    items = my_cursor.fetchall()

                    count = 0

                    for item in items:
                        if count % 2 == 0:
                            my_tree.insert(parent='',index='end',text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12]),tags=('evenrow',))
                        else: 
                            my_tree.insert(parent='',index='end',text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12]),tags=('oddrow',))

                        count += 1

                    conn.commit()
                    conn.close()
            
            busqueda = CTkFrame(self.root, fg_color="transparent")
            busqueda.pack(side="top",fill=X)

            buscar = CTkEntry(busqueda, placeholder_text="Ingrese codigo de alquiler", placeholder_text_color="white",width=200, height=35,text_color="white",
                            fg_color="#005954", border_color="lightgreen")
            buscar.grid(row=0, column=0,pady=10)

            searh = CTkButton(busqueda, text="Buscar",fg_color="#005954", text_color="white",
                                    width=100, height=35,border_color="lightgreen",border_width=2, hover_color="#57bd9e",
                                    font=("Ubuntu",18), command=search_now)
            searh.grid(row=0, column=1, padx=5)
            
            refresh = CTkButton(busqueda, text="Refresh",fg_color="#005954", text_color="white",
                                            width=100, height=35,border_color="lightgreen",border_width=2,
                                            font=("Ubuntu",18), command=actualizar_tree_2)
            refresh.grid(row=0, column=2, padx=5)

            tree_frame = Frame(self.root)
            tree_frame.pack(pady=20, fill=Y, expand=Y)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT,fill=Y)

            bara = Scrollbar(tree_frame, orient=HORIZONTAL)
            bara.pack(side=BOTTOM,fill=X)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, xscrollcommand=bara.set, selectmode="extended",show="headings")
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
            my_tree.heading("TLF", text="Tfno",anchor=CENTER)
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

            
            #for row in rows:
            #    my_tree.insert("", "end", values=row)
            
            count = 0
            for row in rows:
                if count % 2 == 0:
                    my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('evenrow',))#,
                else:
                    my_tree.insert(parent='',index='end',text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags=('oddrow',))
                count += 1

            my_tree.pack()

            self.root.mainloop()
    dato()