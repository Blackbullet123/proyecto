from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from frame_datos import FrameDatosDetallados
from frame_vehiculos import FrameVehiculos
from frame_nuevo_vehiculo import FrameNuevoVehiculo
from frame_mantenimiento import FrameMantenimiento
from frame_respaldo import FrameBackup
from datetime import datetime, timedelta
import os
from pathlib import Path
import webbrowser



def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class Principal:
    def __init__(self):
        self.root = CTk()
        self.root.title('ALQUITECH')
        self.root.geometry("1280x650+35+15")
        # self.root.iconbitmap("imagenes/letra-r.ico")
        self.root.config(background="#EEEEEE")

        self.barra_visible = True
        self.barra_width = 230
        self.velocidad = 11 


        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "tu_nueva_contraseña",
            port = "3306",
            database = "control_alquiler_Reych"
        )

        my_cursor = mydb.cursor()


        def query_db():
            conn = mydb

            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID;")
            records = my_cursor.fetchall()

            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]),tags=('evenrow',))
                else: 
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]),tags=('oddrow',))

                count += 1

            conn.commit()
            conn.close()


        style = ttk.Style()

        style.theme_use('clam')

        style.configure(
            "Treeview",
            background="#d5ffff",
            foreground="black",
            rowheight=25,
            fieldbackground="#FCFCFC"
        )

        style.map('Treeview',
                background=[('selected',"#00501B")])
        
        def update():
                        
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql = "UPDATE alquiler SET COD_Alquiler='{0}',Fecha='{1}',Fecha_Expiracion='{2}' WHERE COD_Alquiler = '{0}'"
            #my_cursor.execute(sql.format(COD_entry.get(),fi_entry.get(),ff_entry.get()))
            #conn.commit()
            #conn.close()

            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql2 = "UPDATE contratista SET RIF='{0}', nombre='{1}', telefono='{2}' WHERE RIF='{0}'"
            #my_cursor.execute(sql.format(rif_entry.get(),em_entry.get(),tlf_entry.get(),rif_entry.get()))
            #conn.commit()
            #conn.close()

            try:
                my_cursor.execute(sql.format(COD_entry.get(),))#fi_entry.get(),ff_entry.get()))
                conn.commit()
                #conn.close()
                my_cursor.execute(sql2.format(rif_entry.get(),em_entry.get(),tlf_entry.get(),rif_entry.get()))
                conn.commit()
                #conn.close()
                titulo = 'Alquilado'
                mensaje = 'Actualizado con exito'
                messagebox.showinfo(titulo, mensaje)
            except:
                titulo = 'Alquilado'
                mensaje = 'Ocurrio un problema'
                messagebox.showinfo(titulo, mensaje)
            finally:
                actualizar_tree()

            

            COD_entry.delete(0,END)
            #fi_entry.delete(0,END)
            #ff_entry.delete(0,END)
            rif_entry.delete(0,END)
            em_entry.delete(0,END)
            tlf_entry.delete(0,END)
            ci_entry.delete(0,END)
            placa_entry.delete(0,END)
            marca_entry.delete(0,END)
            model_entry.delete(0,END)

        def remove_one():
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql = "DELETE FROM alquiler WHERE COD_Alquiler = '{0}'"


            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql2 = "DELETE FROM contratista WHERE RIF = '{0}'"
            #my_cursor.execute(sql2.format(rif_entry.get()))
            #conn.commit()
            #conn.close()
            
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql3 = "DELETE FROM representante WHERE CI = '{0}'"

            try:
                my_cursor.execute(sql.format(COD_entry.get()))
                conn.commit()
                #conn.close()
                my_cursor.execute(sql2.format(rif_entry.get()))
                conn.commit()
                #conn.close()
                my_cursor.execute(sql3.format(ci_entry.get()))
                conn.commit()
                #conn.close()
                titulo = 'Alquilado'
                mensaje = 'Vehiculo eliminado con exito'
                messagebox.showinfo(titulo, mensaje)
            except:
                titulo = 'Alquilado'
                mensaje = 'Ocurrio un problema'
                messagebox.showinfo(titulo, mensaje)
            finally:
                actualizar_tree()

        def clear_entries():
            COD_entry.delete(0,END)
            #fi_entry.delete(0,END)
            #ff_entry.delete(0,END)
            rif_entry.delete(0,END)
            em_entry.delete(0,END)
            tlf_entry.delete(0,END)
            ci_entry.delete(0,END)
            placa_entry.delete(0,END)
            marca_entry.delete(0,END)
            model_entry.delete(0,END)
            self.ocultar_botones()

        def select_record(e):
            COD_entry.delete(0,END)
            #fi_entry.delete(0,END)
            #ff_entry.delete(0,END)
            rif_entry.delete(0,END)
            em_entry.delete(0,END)
            tlf_entry.delete(0,END)
            ci_entry.delete(0,END)
            placa_entry.delete(0,END)
            marca_entry.delete(0,END)
            model_entry.delete(0,END)

            selected = my_tree.focus()
            values = my_tree.item(selected,'values')

            COD_entry.insert(0,values[0])
            #fi_entry.insert(0, values[1])
            #ff_entry.insert(0, values[2])
            rif_entry.insert(0, values[3])
            em_entry.insert(0, values[4])
            tlf_entry.insert(0, values[5])
            ci_entry.insert(0, values[6])
            placa_entry.insert(0, values[7])
            marca_entry.insert(0, values[8])
            model_entry.insert(0, values[9])
            self.mostrar_btn()

        
        frame_form = Frame(self.root,bd=0,relief=SOLID,bg="#000000",height=50)
        frame_form.pack(side="top",expand=NO,fill=BOTH)
        
        frame_ocultar = Frame(frame_form, bd=0, bg="#000000" )
        frame_ocultar.pack(side="top",expand=NO,fill=BOTH)

        frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='#000000')
        frame_form_top.pack(side="top",fill=X)

        self.frame_form_left = CTkFrame(self.root,fg_color='#000000',height=50, width=self.barra_width)
        self.frame_form_left.pack(side="left",fill=Y)# pady=20
        self.frame_form_left.pack_propagate(False)

        self.frame_main = CTkFrame(self.root, fg_color='#EEEEEE')
        self.frame_main.pack(side="left", fill="both", expand=True)

        self.frame_form_l = CTkFrame(self.frame_form_left, fg_color="#000000")
        self.frame_form_l.pack(side="left", fill=Y)

        self.frame_principal = CTkFrame(self.frame_main, fg_color="#EEEEEE")
        self.frame_principal.pack(side="left", fill="both", expand=True)

        self.frame_nuevo_vehiculo = FrameNuevoVehiculo(self.frame_main, self)
        self.frame_datos_detallados = FrameDatosDetallados(self.frame_principal, self)
        self.frame_vehiculos_disponibles = FrameVehiculos(self.frame_main, self)
        self.frame_mantenimeinto = FrameMantenimiento(self.frame_main, self)
        self.frame_backup = FrameBackup(self.frame_main, self)


        frame_top = CTkFrame(self.frame_form_l, fg_color="#000000")
        frame_top.pack(side="top",fill=X, padx=10)

        title = CTkLabel(master=frame_top,text="Alquitech",font=('times new roman',40),text_color="white")#008259  ff8c69
        title.pack(expand=YES,fill=BOTH,padx=30)

        frame_top2 = CTkFrame(frame_top, fg_color="transparent", border_width=0,height=80)
        frame_top2.pack(side="top",fill=X)

        imglogo = Image.open("imagenes/Reych.png")
        imglogo = imglogo.crop(imglogo.getbbox())

        logo_frame = CTkFrame(frame_top2, fg_color="transparent",width=10, height=10)#fg_color="transparent",
        logo_frame.pack(side="top",fill=X, padx=5)

        bg = CTkLabel(master=logo_frame, text=None,image=CTkImage(dark_image=imglogo, light_image=imglogo, size=(140,140)))
        bg.pack(anchor="center", padx=10, pady=25)

        frame_botones = CTkFrame(self.frame_form_l, fg_color="transparent")
        frame_botones.pack(side="top",fill=X, pady=20)

        img = Image.open("imagenes/hogar.png")
        inicio_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        inicio = CTkButton(frame_botones, text="Inicio",fg_color="transparent",text_color="white",
                                  width=150, height=30,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=inicio_icon, compound="left",
                                  command=self.mostrar_contenido_principal)
        inicio.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/alquiler.png")
        alquilar_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        alquilar = CTkButton(frame_botones, text="Alquilar",fg_color="transparent",text_color="white",
                                  width=150, height=30,hover_color="#00501B",
                                  font=("Ubuntu",17),anchor=W, image=alquilar_icon, compound="left",
                                    command=self.mostrar_vehiculos_disponibles)
        alquilar.pack(pady=5, padx=2, fill=X)

        '''img = Image.open("imagenes/registro.png")
        datos_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        date_detalles = CTkButton(frame_botones, text="Datos detallados",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=datos_icon, compound="left",
                                  command=self.mostrar_datos_detallados)
        date_detalles.pack(pady=5, padx=2, fill=X)'''

        img = Image.open("imagenes/nuevo.png")
        nuevo_vehiculo_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        nuevo_vehiculo = CTkButton(frame_botones, text="Nuevo Vehiculo",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B", command=self.mostrar_nuevo_vehiculo,
                                  font=("Ubuntu",17), anchor=W, image=nuevo_vehiculo_icon, compound="left")
        nuevo_vehiculo.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/backup.png")
        backup_restore_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        backup_restore = CTkButton(frame_botones, text="Backup y Restore",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=backup_restore_icon, compound="left",
                                  command=self.mostrar_respaldo)
        backup_restore.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/mantenimiento.png")
        mantenimiento_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        mantenimiento = CTkButton(frame_botones, text="Mantenimiento",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=mantenimiento_icon, compound="left",
                                  command=self.mostrar_mantenimiento)
        mantenimiento.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/ayuda.png")
        ayuda_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        ayuda = CTkButton(frame_botones, text="Ayuda",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=ayuda_icon, compound="left"
                                  , command=abrir_pdf)
        ayuda.pack(pady=5,padx=2, fill=X)

        self.ocultar_btn = CTkButton(frame_ocultar, text="☰ Ocultar",
                                     text_color="white", fg_color="#0E0F0F",hover_color="#00501B",
                                     command=self.toggle_barra)
        self.ocultar_btn.pack(anchor="nw", padx=10, pady=10, side=LEFT)



        def romper():
            self.root.destroy()

            from forms.form_login import App

            App()

            

        frame_botones2 = CTkFrame(self.frame_form_l, fg_color="transparent")
        frame_botones2.pack(side="bottom",fill=X, pady=20)

        img = Image.open("imagenes/salir.png")
        salir = CTkImage(dark_image=img, light_image=img, size=(24,24))
        boton = CTkButton(frame_botones2, text="Cerrar Sesión",fg_color="transparent", text_color="white",
                                  width=100, height=30,hover_color="#00501B",
                                  font=("Ubuntu",18), command=romper,image=salir, compound="left")
        boton.pack(pady=5, padx=2, side="left")


        
        #frame superior de botones
        button_frame = Frame(self.frame_principal, bg="#EEEEEE")
        button_frame.pack(expand=True,padx=20, pady=0,fill=X)

        titulo = CTkLabel(button_frame, text="ALQUITECH",
                        text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        frame_contenedor_ver = Frame(self.frame_principal,bg="#EEEEEE",width=30, height=30)
        frame_contenedor_ver.pack(fill="x", expand=NO, padx=20)

        frame_ver_mas = Frame(frame_contenedor_ver,bg="#EEEEEE",width=90, height=30)
        frame_ver_mas.pack(expand=NO, side=RIGHT)

        def actualizar_tree():
            for item in my_tree.get_children():
                my_tree.delete(item)

                mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "tu_nueva_contraseña",
                port = "3306",
                database = "control_alquiler_Reych"
            )

            conn = mydb

            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID;")
            items = my_cursor.fetchall()

            count = 0

            for item in items:
                if count % 2 == 0:
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9]),tags=('evenrow',))
                else: 
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9]),tags=('oddrow',))

                count += 1

            conn.commit()
            conn.close()

        def search_now():
                
                for item in my_tree.get_children():
                    my_tree.delete(item)

                mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "tu_nueva_contraseña",
                    port = "3306",
                    database = "control_alquiler_Reych"
                )
                my_cursor = mydb.cursor()
                conn = mydb
                sql = "SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID WHERE COD_Alquiler = {0}"

                my_cursor.execute(sql.format(buscar.get()))
                records = my_cursor.fetchall()
                
                
                for record in records:
                                my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]))#,


                conn.commit()
                conn.close()


        buscar_label = CTkLabel(button_frame, text="Buscar Vehículo:",
                                text_color="black", font=("Ubuntu", 15))
        buscar_label.pack(side="left", padx=5, pady=10)

        buscar = CTkEntry(button_frame, width=250)
        buscar.pack(side="left", padx=5)

        searh = CTkButton(button_frame, text="Buscar",
                               fg_color="#0E0F0F", font=("Ubuntu",13), text_color="white", hover_color="#00501B",
                               width=100, height=30, command=search_now)
        searh.pack(side="left", padx=10)

        img = Image.open("imagenes/imprimir.png")
        imprimir_icon = CTkImage(dark_image=img, light_image=img, size=(40,40))
        imprimir = CTkButton(button_frame, hover_color="#EEEEEE" ,image=imprimir_icon , text="", fg_color="transparent",
                               width=30, height=30, )#command=imprimir_vehiculos)
        imprimir.pack(side="right", padx=3)

        #treeview
        self.tree_frame = Frame(self.frame_principal, bg="#EEEEEE")
        self.tree_frame.pack(pady=0, expand=True, fill=BOTH)

        tree_scroll = Scrollbar(self.tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=tree_scroll.set,
            selectmode="extended",
            show="headings"
        )
        my_tree.pack(fill=BOTH, expand=True)

        tree_scroll.config(command=my_tree.yview)

        tree_scroll.config(command=my_tree.yview)

        #CREACION DE COLUMNAS
        my_tree['columns']=("COD","FechaI","FechaF","RIF","Empresa","TLF","CI","Placa","Modelo","Marca")#

        my_tree.column("COD",anchor=CENTER,width=85)
        my_tree.column("FechaI",anchor=CENTER,width=85)
        my_tree.column("FechaF",anchor=CENTER,width=85)
        my_tree.column("RIF",anchor=CENTER,width=140)
        my_tree.column("Empresa",anchor=CENTER,width=120)
        my_tree.column("TLF",anchor=CENTER,width=120)
        my_tree.column("CI",anchor=CENTER,width=120)
        my_tree.column("Placa",anchor=CENTER,width=120)
        my_tree.column("Modelo",anchor=CENTER,width=120)
        my_tree.column("Marca",anchor=CENTER,width=120)

        my_tree.heading("COD", text="Cod.",anchor=CENTER)
        my_tree.heading("FechaI", text="Fecha Inicial",anchor=CENTER)
        my_tree.heading("FechaF", text="Fecha Final",anchor=CENTER)
        my_tree.heading("RIF", text="RIF",anchor=CENTER)
        my_tree.heading("Empresa", text="Empresa",anchor=CENTER)
        my_tree.heading("TLF", text="Teléfono",anchor=CENTER)
        my_tree.heading("CI", text="Cedula",anchor=CENTER)
        my_tree.heading("Placa", text="Placa",anchor=CENTER)
        my_tree.heading("Modelo", text="Vehículo Modelo",anchor=CENTER)
        my_tree.heading("Marca", text="Vehículo Marca",anchor=CENTER)

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#00501B")



        def validate_entry2(text,new_text):
            if len(new_text) > 3:#Hace que no supere los 10 digitos
                return False
            return text.isdecimal()

        def validate_entry(text,new_text):
            if len(new_text) > 15:#Hace que no supere los 10 digitos
                return False
            return text.isdecimal()
        
        def validate_fecha(new_text):
            if len(new_text) > 10:
                return False
            checks = []
            for i, char in enumerate (new_text):
                if i in (5 , 2):
                    checks.append(char == "-")
                else:
                    checks.append(char.isdecimal())
            return all(checks)
        
        #Frame de los inferior    

        frame_inferior = Frame(self.frame_principal,bg="#EEEEEE")
        frame_inferior.pack(fill="x", expand=True, padx=70, side="bottom")

        self.frame_botones_inferiores = CTkFrame(frame_inferior, fg_color="#EEEEEE", width=100, height=40)
        self.frame_botones_inferiores.pack( anchor="center", expand=True)

        self.data_frame = CTkFrame(frame_inferior, fg_color="transparent")
        self.data_frame.pack(anchor="center", expand=True)

        self.frame_contenedor_entry = CTkFrame(frame_inferior, fg_color="transparent")
        self.frame_contenedor_entry.pack(anchor="center", expand=True)

        COD_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=100, height=20)
        COD_frame.grid(row=1, column=4, padx=25,pady=4, ipady=3)

        COD_label = CTkLabel(COD_frame, text="Cod.",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        COD_label.grid(row=0, column=0, padx=10, pady=1)
        COD_entry = CTkEntry(COD_frame,justify=CENTER,width=130, state=DISABLED ,fg_color="transparent",text_color="black", border_color="#00501B",
                             validate="key", validatecommand=(self.data_frame.register(validate_entry2), "%S","%P"))
        COD_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha1_frame = CTkFrame(self.frame_contenedor_entry, fg_color="transparent",corner_radius=6, width=100, height=20)
        fecha1_frame.grid(row=0, column=1,padx=25,pady=4, ipady=3)

        fi_label = CTkLabel(fecha1_frame, text="Fecha Inicial",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        fi_label.grid(row=0,column=0, padx=10, pady=1)
        fi_entry = CTkEntry(fecha1_frame,justify=CENTER,fg_color="transparent",text_color="black", width=130, border_color="#00501B",
                            validate="key", validatecommand=(self.data_frame.register(validate_fecha), "%P"))
        fi_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha2_frame = CTkFrame(self.frame_contenedor_entry, fg_color="transparent",corner_radius=6, width=50, height=20,)
        fecha2_frame.grid(row=0, column=2,padx=25,pady=4, ipady=3)

        ff_label = CTkLabel(fecha2_frame, text="Fecha Final",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        ff_label.grid(row=0,column=0, padx=10, pady=1)
        ff_entry = CTkEntry(fecha2_frame, justify=CENTER,fg_color="transparent",text_color="black", width=130, border_color="#00501B",
                            validate="key", validatecommand=(self.data_frame.register(validate_fecha), "%P"))
        ff_entry.grid(row=1,column=0, padx=10, pady=1)

        self.ocultar_entry()

        rif_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6,  width=50, height=20,)
        rif_frame.grid(row=0, column=1,padx=25,pady=4, ipady=3)

        rif_label = CTkLabel(rif_frame, text="RIF",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        rif_label.grid(row=0,column=0, padx=10, pady=1)
        rif_entry = CTkEntry(rif_frame, justify=CENTER,fg_color="transparent", text_color="black", width=130,  border_color="#00501B",
                             validate="key", validatecommand=(self.data_frame.register(validate_entry), "%S","%P"))
        rif_entry.grid(row=1,column=0, padx=10, pady=1)

        empresa_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=35, height=20,)
        empresa_frame.grid(row=0, column=2,padx=25,pady=4, ipady=3)

        em_label = CTkLabel(empresa_frame, text="Empresa",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        em_label.grid(row=0,column=0, padx=10, pady=1)
        em_entry = CTkEntry(empresa_frame, justify=CENTER,fg_color="transparent",text_color="black", border_color="#00501B",
                            width=130)
        em_entry.grid(row=1,column=0, padx=10, pady=1)
        
        ci_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20)
        ci_frame.grid(row=0, column=4, padx=25,pady=4, ipady=3)

        ci_label = CTkLabel(ci_frame, text="Cedula",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        ci_label.grid(row=0, column=0, padx=10, pady=1)
        ci_entry = CTkEntry(ci_frame,justify=CENTER,width=130,fg_color="transparent",text_color="black", border_color="#00501B",
                             validate="key", validatecommand=(self.data_frame.register(validate_entry), "%S","%P"))
        ci_entry.grid(row=1,column=0, padx=10, pady=1)

        tlf_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        tlf_frame.grid(row=0, column=3,padx=25,pady=4, ipady=3)

        tlf_label = CTkLabel(tlf_frame, text="Teléfono",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        tlf_label.grid(row=0,column=0, padx=10, pady=1)
        tlf_entry = CTkEntry(tlf_frame,justify=CENTER, fg_color="transparent",text_color="black", width=130, border_color="#00501B",
                             validate="key", validatecommand=(self.data_frame.register(validate_entry), "%S","%P"))
        tlf_entry.grid(row=1,column=0, padx=10, pady=1)

        placa_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        placa_frame.grid(row=1, column=1,padx=10,pady=4, ipady=3)

        placa_label = CTkLabel(placa_frame, text="Placa",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        placa_label.grid(row=0,column=0, padx=10, pady=1)
        placa_entry = CTkEntry(placa_frame, justify=CENTER,fg_color="transparent", text_color="black", width=130, border_color="#00501B",)
        placa_entry.grid(row=1,column=0, padx=10, pady=1)

        marca_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        marca_frame.grid(row=1, column=2,padx=10,pady=4, ipady=3)

        marca_label = CTkLabel(marca_frame, text="Marca",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        marca_label.grid(row=0,column=0, padx=10, pady=1)
        marca_entry = CTkEntry(marca_frame, justify=CENTER,fg_color="transparent", text_color="black",width=130, border_color="#00501B",)
        marca_entry.grid(row=1,column=0, padx=10, pady=1)

        model_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        model_frame.grid(row=1, column=3,padx=10,pady=4, ipady=3)

        model_label = CTkLabel(model_frame, text="Modelo",fg_color="transparent",text_color="#00501B",
                                    font=("Ubuntu",16))
        model_label.grid(row=0,column=0, padx=10, pady=1)
        model_entry = CTkEntry(model_frame,justify=CENTER, fg_color="transparent", text_color="black",width=130, border_color="#00501B",)
        model_entry.grid(row=1,column=0, padx=10, pady=1)

        self.ver_menos = CTkButton(frame_ver_mas, text="Ver menos",text_color="#00501B", width=20,
                                  height=30,cursor="hand2",command=self.ocultar_datos_detallados,
                                    hover_color="#EEEEEE",fg_color="#EEEEEE", font=("Impact", 16))
        self.ver_menos.place(x=8, y=2)
        self.ocultar_ver_menos()

        self.ver_mas = CTkButton(frame_ver_mas, text="Ver mas",text_color="#00501B", width=20,
                                  height=30,cursor="hand2",command=self.mostrar_datos_detallados,
                                    hover_color="#EEEEEE",fg_color="#EEEEEE", font=("Impact", 16))
        self.ver_mas.place(x=8, y=2)

        self.update_button = CTkButton(self.frame_botones_inferiores, text="Actualizar", command=update,
                          corner_radius=15, text_color="white", width=150, height=40,
                          fg_color="#00A86B", font=("Impact", 16))
        self.update_button.grid(row=0, column=0, padx=20, pady=5)


        self.limpiar = CTkButton(self.frame_botones_inferiores, text="Limpiar", command=clear_entries,
                            corner_radius=15, text_color="white", width=150, height=40,
                            fg_color="#E0DC00", font=("Impact", 16))
        self.limpiar.grid(row=0, column=2, padx=20, pady=5)

        self.remove_one_button = CTkButton(self.frame_botones_inferiores, text="Eliminar", command=remove_one,
                                    corner_radius=15, text_color="white", width=150, height=40,
                                    fg_color="#D32F2F", font=("Impact", 16))
        self.remove_one_button.grid(row=0, column=3, padx=20, pady=5)

        self.renovar = CTkButton(self.frame_botones_inferiores,
                                 command=self.ocultar_renovar,text="Renovar",
                                    corner_radius=15, text_color="white", width=150, height=40,
                                    fg_color="#8200EC", font=("Impact", 16))
        self.renovar.grid(row=0, column=1, padx=20, pady=5)

        #self.ocultar_botones()


        my_tree.bind("<ButtonRelease-1>", select_record)

        query_db()


        self.root.mainloop()


    def toggle_barra(self):
        if self.barra_visible:
            self.frame_form_left.configure(width=0)
            self.ocultar_btn.configure(text="☰ Mostrar")
        else:
            self.frame_form_left.configure(width=self.barra_width)
            self.ocultar_btn.configure(text="☰ Ocultar")
        self.barra_visible = not self.barra_visible

    def mostrar_datos_detallados(self):
        self.tree_frame.pack_forget()
        self.frame_datos_detallados.pack(expand=True, fill=BOTH)
        self.no_ver()

    def ocultar_datos_detallados(self):
        self.frame_datos_detallados.pack_forget()
        self.tree_frame.pack(expand=True, fill=BOTH)
        self.ver()

    def mostrar_vehiculos_disponibles(self):
        self.frame_principal.pack_forget()
        self.frame_backup.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_vehiculos_disponibles.pack(expand=True, fill=BOTH)

    def mostrar_nuevo_vehiculo(self):
        self.frame_principal.pack_forget()
        self.frame_backup.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_nuevo_vehiculo.pack(expand=True, fill=BOTH)

    def mostrar_mantenimiento(self):
        self.frame_principal.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_backup.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_mantenimeinto.pack(expand=True, fill=BOTH)

    def mostrar_respaldo(self):
        self.frame_mantenimeinto.pack_forget()
        self.frame_principal.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_backup.pack(expand=True, fill=BOTH)

    def mostrar_contenido_principal(self):
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_backup.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_principal.pack(expand=True, fill=BOTH)

    def ocultar_botones(self):
        self.frame_botones_inferiores.pack_forget()

    def ocultar_entry(self):
        self.frame_contenedor_entry.pack_forget()

    def ocultar_renovar(self):
        self.data_frame.pack_forget()
        self.frame_contenedor_entry.pack(expand=True, fill=BOTH)

    def mostrar_renovar(self):
        self.frame_contenedor_entry.pack_forget()
        self.data_frame.Pack(expand=True, fill=BOTH)
        

    def mostrar_btn(self):
        self.frame_botones_inferiores.pack()

    def ocultar_ver_menos(self):
        self.ver_menos.place_forget()

    def ver(self):
        self.ver_menos.place_forget()
        self.ver_mas.place(x=10, y=2)

    def no_ver(self):
        self.ver_mas.place_forget()
        self.ver_menos.place(x=10, y=2)


def abrir_pdf():
    ruta_pdf = get_project_root() / "PDF" / "manual.pdf"
    
    if os.path.exists(ruta_pdf):
        os.system(f'start {ruta_pdf}')

pdf_path = get_project_root() / "PDF" / "manual.pdf"        
ruta_pdf = pdf_path

Principal()