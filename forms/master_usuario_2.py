from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from customtkinter import *
from forms.frame_datos import FrameDatosDetallados
from forms.frame_vehiculos import FrameVehiculos
from forms.frame_nuevo_vehiculo import FrameNuevoVehiculo
from forms.frame_mantenimiento import FrameMantenimiento
from forms.frame_estadisticas import FrameEstadisticas
from forms.imprimir import ventana_imprimir
from forms.frame_configuracion import FrameConfiguracion
import os
from tkcalendar import Calendar
from datetime import date, datetime
from pathlib import Path
import webbrowser



def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class usuario:
    def __init__(self):
        self.root = CTk()
        self.root.title('ALQUITECH')
        self.root.geometry("1280x650+35+15")
        self.root.iconbitmap("imagenes/letra-r.ico")
        # El fondo se maneja automáticamente por CTk al cambiar el modo de apariencia



        self.barra_visible = True
        self.barra_width = 230


        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123456",
            port = "3306",
            database = "control_alquiler_Reych"
        )

        my_cursor = mydb.cursor()


        def query_db():
            conn = mydb

            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID ORDER BY a.COD_Alquiler ASC;")
            records = my_cursor.fetchall()

            count = 0

            for record in records:
                if count % 2 == 0:
                    self.my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]),tags=('evenrow',))
                else: 
                    self.my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]),tags=('oddrow',))

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
                background=[('selected',"#008fa8")])

        def clear_entries():
            COD_entry.delete(0,END)
            fi_entry.delete(0,END)
            ff_entry.delete(0,END)
            rif_entry.delete(0,END)
            em_entry.delete(0,END)
            tlf_entry.delete(0,END)
            ci_entry.delete(0,END)
            placa_entry.delete(0,END)
            marca_entry.delete(0,END)
            model_entry.delete(0,END)
            self.ocultar_botones()
            self.actualizar_tree()

        def select_record(e):
            selected = self.my_tree.focus()
            if not selected:
                return

            values = self.my_tree.item(selected, 'values')
            if not values:
                return
            self.mostrar_btn()

            COD_entry.delete(0,END)
            fi_entry.delete(0,END)
            ff_entry.delete(0,END)
            rif_entry.delete(0,END)
            em_entry.delete(0,END)
            tlf_entry.delete(0,END)
            ci_entry.delete(0,END)
            placa_entry.delete(0,END)
            marca_entry.delete(0,END)
            model_entry.delete(0,END)

            COD_entry.insert(0,values[0])
            fi_entry.insert(0, values[1])
            ff_entry.insert(0, values[2])
            rif_entry.insert(0, values[3])
            em_entry.insert(0, values[4])
            tlf_entry.insert(0, values[5])
            ci_entry.insert(0, values[6])
            placa_entry.insert(0, values[7])
            marca_entry.insert(0, values[8])
            model_entry.insert(0, values[9])
        

        def remove_one():
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                port = "3306",
                database = "control_alquiler_Reych"
            )
            my_cursor = mydb.cursor()
            conn = mydb
            sql = "DELETE FROM alquiler WHERE COD_Alquiler = '{0}'"
            #my_cursor.execute(sql.format(COD_entry.get()))
            #conn.commit()
            #conn.close()

            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
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
                password = "123456",
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
                titulo = 'error'
                mensaje = 'Ocurrio un problema'
                messagebox.showerror(titulo, mensaje)
            finally:
                self.actualizar_tree()
                clear_entries()
        
        
        def update():
                        
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
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
                password = "123456",
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
                my_cursor.execute(sql.format(COD_entry.get(),fi_entry.get(),ff_entry.get()))
                conn.commit()
                #conn.close()
                my_cursor.execute(sql2.format(rif_entry.get(),em_entry.get(),tlf_entry.get(),rif_entry.get()))
                conn.commit()
                #conn.close()
                titulo = 'Alquilado'
                mensaje = 'Actualizado con exito'
                messagebox.showinfo(titulo, mensaje)
            except:
                titulo = 'error'
                mensaje = 'Ocurrio un problema'
                messagebox.showerror(titulo, mensaje)
            finally:
                self.actualizar_tree()
                self.frame_estadisticas.actualizar_grafico()
                clear_entries()

            
        
        frame_form = Frame(self.root,bd=0,relief=SOLID,bg="#000000",height=50)
        frame_form.pack(side="top",expand=NO,fill=BOTH)
        
        frame_ocultar = Frame(frame_form, bd=0, bg="#000000" )
        frame_ocultar.pack(side="top",expand=NO,fill=BOTH)

        frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='#000000')
        frame_form_top.pack(side="top",fill=X)

        self.frame_form_left = CTkFrame(self.root,fg_color='#000000',height=50, width=self.barra_width)
        self.frame_form_left.pack(side="left",fill=Y)# pady=20
        self.frame_form_left.pack_propagate(False)

        self.frame_main = CTkFrame(self.root, fg_color=("#EEEEEE", "#1A1A1A"))

        self.frame_main.pack(side="left", fill="both", expand=True)

        self.frame_form_l = CTkFrame(self.frame_form_left, fg_color="#000000")
        self.frame_form_l.pack(side="left", fill=Y)

        self.frame_principal = CTkFrame(self.frame_main, fg_color=("#EEEEEE", "#1A1A1A"))

        self.frame_principal.pack(side="left", fill="both", expand=True)

        self.frame_nuevo_vehiculo = FrameNuevoVehiculo(self.frame_main, self)
        self.frame_datos_detallados = FrameDatosDetallados(self.frame_principal, self)
        self.frame_vehiculos_disponibles = FrameVehiculos(self.frame_main,self)
        self.frame_mantenimeinto = FrameMantenimiento(self.frame_main, self)
        self.frame_configuracion = FrameConfiguracion(self.frame_main, self)
        self.frame_estadisticas = FrameEstadisticas(self.frame_main, self)


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


        img = Image.open("imagenes/nuevo.png")
        nuevo_vehiculo_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        nuevo_vehiculo = CTkButton(frame_botones, text="Nuevo Vehiculo",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B", command=self.mostrar_nuevo_vehiculo,
                                  font=("Ubuntu",17), state=DISABLED,anchor=W, image=nuevo_vehiculo_icon, compound="left")
        nuevo_vehiculo.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/mantenimiento.png")
        mantenimiento_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        mantenimiento = CTkButton(frame_botones, text="Mantenimiento",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=mantenimiento_icon, compound="left",
                                  command=self.mostrar_mantenimiento)
        mantenimiento.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/estadisticas.png")
        datos_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        date_detalles = CTkButton(frame_botones, text="Estadisticas",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=datos_icon, compound="left",
                                  command=self.mostrar_estadisticas)
        date_detalles.pack(pady=5, padx=2, fill=X)

        img = Image.open("imagenes/configuraciones.png")
        configuracion_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        configuracion = CTkButton(frame_botones, text="Configuración",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=configuracion_icon, compound="left",
                                  command=self.mostrar_configuracion)
        configuracion.pack(pady=5, padx=2, fill=X)

        '''img = Image.open("imagenes/ayuda.png")
        ayuda_icon = CTkImage(dark_image=img, light_image=img, size=(24,24))
        ayuda = CTkButton(frame_botones, text="Ayuda",fg_color="transparent",text_color="white",
                                  width=150, height=40,hover_color="#00501B",
                                  font=("Ubuntu",17), anchor=W, image=ayuda_icon, compound="left"
                                  , command=abrir_pdf)
        ayuda.pack(pady=5,padx=2, fill=X)'''

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
        button_frame = CTkFrame(self.frame_principal, fg_color=("#EEEEEE", "#1A1A1A"))

        button_frame.pack(expand=True,padx=20, pady=0,fill=X)

        titulo = CTkLabel(button_frame, text="ALQUITECH",
                        text_color=("#00501B", "#00FF7F"), font=("Impact", 45))

        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        frame_contenedor_renovar = CTkFrame(self.frame_principal,fg_color=("#EEEEEE", "#1A1A1A"),width=30, height=30)

        frame_contenedor_renovar.pack(fill="x", expand=NO, padx=20)

        frame_renovar = CTkFrame(frame_contenedor_renovar,fg_color=("#EEEEEE", "#1A1A1A"),width=150, height=30)

        frame_renovar.pack(expand=NO, side=LEFT)

        frame_ver_mas = CTkFrame(frame_contenedor_renovar,fg_color=("#EEEEEE", "#1A1A1A"),width=90, height=30)

        frame_ver_mas.pack(expand=NO, side=RIGHT)


        def search_now():
                
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
            conn = mydb
            sql = "SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID WHERE COD_Alquiler = {0}"

            my_cursor.execute(sql.format(buscar.get()))
            records = my_cursor.fetchall()
            
            
            for record in records:
                            self.my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9]))


            conn.commit()
            conn.close()


        buscar_label = CTkLabel(button_frame, text="Buscar:",
                                text_color=("black", "white"), font=("Ubuntu", 15))
        buscar_label.pack(side="left", padx=5, pady=10)

        buscar = CTkEntry(button_frame, width=250, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")

        buscar.pack(side="left", padx=5)

        searh = CTkButton(button_frame, text="Buscar",
                               fg_color="#0E0F0F", font=("Ubuntu",13), text_color="white", hover_color="#00501B",
                               width=100, height=30, command=search_now)
        searh.pack(side="left", padx=10)

        img = Image.open("imagenes/imprimir.png")
        img_white = Image.open("imagenes/imprimir_white.png")
        imprimir_icon = CTkImage(light_image=img, dark_image=img_white, size=(40,40))

        imprimir = CTkButton(button_frame, hover_color=("#EEEEEE", "#2D2D2D"),command=ventana_imprimir ,image=imprimir_icon , text="", fg_color="transparent",

                               width=30, height=30, )
        imprimir.pack(side="right", padx=3)

        #treeview
        self.tree_frame = Frame(self.frame_principal, bg="#EEEEEE")
        self.tree_frame.pack(pady=0, expand=True, fill=BOTH)

        tree_scroll = Scrollbar(self.tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=tree_scroll.set,
            selectmode="extended",
            show="headings"
        )
        self.my_tree.pack(fill=BOTH, expand=True)

        tree_scroll.config(command=self.my_tree.yview)

        tree_scroll.config(command=self.my_tree.yview)

        #CREACION DE COLUMNAS
        self.my_tree['columns']=("COD","FechaI","FechaF","RIF","Empresa","TLF","CI","Placa","Modelo","Marca")

        self.my_tree.column("COD",anchor=CENTER,width=85)
        self.my_tree.column("FechaI",anchor=CENTER,width=75)
        self.my_tree.column("FechaF",anchor=CENTER,width=75)
        self.my_tree.column("RIF",anchor=CENTER,width=120)
        self.my_tree.column("Empresa",anchor=CENTER,width=120)
        self.my_tree.column("TLF",anchor=CENTER,width=120)
        self.my_tree.column("CI",anchor=CENTER,width=120)
        self.my_tree.column("Placa",anchor=CENTER,width=120)
        self.my_tree.column("Modelo",anchor=CENTER,width=120)
        self.my_tree.column("Marca",anchor=CENTER,width=120)

        self.my_tree.heading("COD", text="Cod.",anchor=CENTER)
        self.my_tree.heading("FechaI", text="Fecha Inicial",anchor=CENTER)
        self.my_tree.heading("FechaF", text="Fecha Final",anchor=CENTER)
        self.my_tree.heading("RIF", text="RIF",anchor=CENTER)
        self.my_tree.heading("Empresa", text="Empresa",anchor=CENTER)
        self.my_tree.heading("TLF", text="Teléfono",anchor=CENTER)
        self.my_tree.heading("CI", text="Cedula",anchor=CENTER)
        self.my_tree.heading("Placa", text="Placa",anchor=CENTER)
        self.my_tree.heading("Marca", text="Vehículo Marca",anchor=CENTER)
        self.my_tree.heading("Modelo", text="Vehículo Modelo",anchor=CENTER)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#00A86B")



        def validate_entry2(text,new_text):
            if len(new_text) > 3:
                return False
            return text.isdecimal()

        def validate_entry(text,new_text):
            if len(new_text) > 15:
                return False
            return text.isdecimal()
        
        def abrir_calendario(event, entry):
            top = tk.Toplevel(self.root)
            top.title("Seleccionar fecha")
            top.geometry("290x250+650+300")
            top.grab_set()

            cal = Calendar(top, date_pattern="yyyy-mm-dd", mindate=date.today())
            cal.pack(padx=10, pady=10)

            def seleccionar_fecha():
                fecha = cal.get_date()
                entry.configure(state="normal")
                entry.delete(0, "end")
                entry.insert(0, fecha)
                entry.configure(state="readonly")
                top.destroy()

            btn = CTkButton(top, text="Seleccionar", command=seleccionar_fecha)
            btn.pack(pady=5)


        def get_current_date():
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            fi_entry.delete(0, "end")            
            fi_entry.insert(0, fecha_actual)
            self.root.after(1000, get_current_date)

        #Esto es para las mayusculas ;)
        def mayusculas(event, entry):
            text = entry.get()
            if text:
                entry.delete(0, tk.END)
                entry.insert(0, text[0].upper() + text[1:])

        
        #Frame de los inferior    
        frame_inferior = Frame(self.frame_principal,bg=("#EEEEEE", "#1A1A1A"))
        frame_inferior.pack(fill="x", expand=True, padx=70, side="bottom")

        self.data_frame = CTkFrame(frame_inferior, fg_color="transparent")
        self.data_frame.pack(anchor="center", expand=True)

        self.frame_contenedor_entry = CTkFrame(frame_inferior, fg_color=("#EEEEEE", "#1A1A1A"))
        self.frame_contenedor_entry.pack(anchor="center", side="left",expand=NO)

        self.frame_contenedor_entry_fecha = CTkFrame(self.frame_contenedor_entry, fg_color=("#EEEEEE", "#1A1A1A"))
        self.frame_contenedor_entry_fecha.pack(anchor="center", side="top",expand=NO)

        self.frame_botones_inferiores = CTkFrame(frame_inferior, fg_color=("#EEEEEE", "#1A1A1A"), width=100, height=40)
        self.frame_botones_inferiores.pack( anchor="center", expand=NO)

        COD_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=100, height=20)
        COD_frame.grid(row=1, column=4, padx=25,pady=4, ipady=3)

        COD_label = CTkLabel(COD_frame, text="Cod.",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        COD_label.grid(row=0, column=0, padx=10, pady=1)
        COD_entry = CTkEntry(COD_frame,justify=CENTER,width=130 ,fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), border_color="#00501B",
                             validate="key", validatecommand=(self.data_frame.register(validate_entry2), "%S","%P"))
        COD_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha1_frame = CTkFrame(self.frame_contenedor_entry_fecha, fg_color="transparent",corner_radius=6, width=100, height=20)
        fecha1_frame.grid(row=0, column=1,padx=25,pady=4, ipady=3)

        fi_label = CTkLabel(fecha1_frame, text="Fecha Inicial",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        fi_label.grid(row=0,column=0, padx=10, pady=1)
        fi_entry = CTkEntry(fecha1_frame,justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), width=130, border_color="#00501B")
        fi_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha2_frame = CTkFrame(self.frame_contenedor_entry_fecha, fg_color="transparent",corner_radius=6, width=50, height=20,)
        fecha2_frame.grid(row=0, column=2,padx=25,pady=4, ipady=3)

        ff_label = CTkLabel(fecha2_frame, text="Fecha Final",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        ff_label.grid(row=0,column=0, padx=10, pady=1)
        ff_entry = CTkEntry(fecha2_frame, justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), width=130, border_color="#00501B")
        ff_entry.grid(row=1,column=0, padx=10, pady=1)
        self.ocultar_entry()

        rif_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6,  width=50, height=20,)
        rif_frame.grid(row=0, column=1,padx=25,pady=4, ipady=3)

        rif_label = CTkLabel(rif_frame, text="RIF",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        rif_label.grid(row=0,column=0, padx=10, pady=1)
        rif_entry = CTkEntry(rif_frame, justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), width=130,  border_color="#00501B")
        rif_entry.grid(row=1,column=0, padx=10, pady=1)

        empresa_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=35, height=20,)
        empresa_frame.grid(row=0, column=2,padx=25,pady=4, ipady=3)

        em_label = CTkLabel(empresa_frame, text="Empresa",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        em_label.grid(row=0,column=0, padx=10, pady=1)
        em_entry = CTkEntry(empresa_frame, justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), border_color="#00501B",
                            width=130)
        em_entry.grid(row=1,column=0, padx=10, pady=1)
        
        ci_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20)
        ci_frame.grid(row=0, column=4, padx=25,pady=4, ipady=3)

        ci_label = CTkLabel(ci_frame, text="Cedula",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        ci_label.grid(row=0, column=0, padx=10, pady=1)
        ci_entry = CTkEntry(ci_frame,justify=CENTER,width=130,fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), border_color="#00501B")
        ci_entry.grid(row=1,column=0, padx=10, pady=1)

        tlf_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        tlf_frame.grid(row=0, column=3,padx=25,pady=4, ipady=3)

        tlf_label = CTkLabel(tlf_frame, text="Teléfono",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        tlf_label.grid(row=0,column=0, padx=10, pady=1)
        tlf_entry = CTkEntry(tlf_frame,justify=CENTER, fg_color=("#c2f1c1", "#2D2D2D"),text_color=("black", "white"), width=130, border_color="#00501B")
        tlf_entry.grid(row=1,column=0, padx=10, pady=1)

        placa_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        placa_frame.grid(row=1, column=1,padx=10,pady=4, ipady=3)

        placa_label = CTkLabel(placa_frame, text="Placa",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        placa_label.grid(row=0,column=0, padx=10, pady=1)
        placa_entry = CTkEntry(placa_frame, justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), width=130, border_color="#00501B",)
        placa_entry.grid(row=1,column=0, padx=10, pady=1)

        marca_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        marca_frame.grid(row=1, column=2,padx=10,pady=4, ipady=3)

        marca_label = CTkLabel(marca_frame, text="Marca",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        marca_label.grid(row=0,column=0, padx=10, pady=1)
        marca_entry = CTkEntry(marca_frame, justify=CENTER,fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"),width=130, border_color="#00501B",)
        marca_entry.grid(row=1,column=0, padx=10, pady=1)

        model_frame = CTkFrame(self.data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        model_frame.grid(row=1, column=3,padx=10,pady=4, ipady=3)

        model_label = CTkLabel(model_frame, text="Modelo",fg_color="transparent",text_color=("black", "white"),
                                    font=("Ubuntu",16))
        model_label.grid(row=0,column=0, padx=10, pady=1)
        model_entry = CTkEntry(model_frame,justify=CENTER, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"),width=130, border_color="#00501B",)
        model_entry.grid(row=1,column=0, padx=10, pady=1)

        self.ver_menos = CTkButton(frame_ver_mas, text="Ver menos",text_color="#00501B", width=20,
                                  height=30,cursor="hand2",command=self.ocultar_datos_detallados,
                                    hover_color="#EEEEEE",fg_color=("#EEEEEE", "#1A1A1A"), font=("Impact", 16))
        self.ver_menos.place(x=8, y=2)
        self.ocultar_ver_menos()

        self.ver_mas = CTkButton(frame_ver_mas, text="Ver mas",text_color="#00501B", width=20,
                                  height=30,cursor="hand2",command=self.mostrar_datos_detallados,
                                    hover_color="#EEEEEE",fg_color=("#EEEEEE", "#1A1A1A"), font=("Impact", 16))
        self.ver_mas.place(x=8, y=2)

        self.renovar_menos = CTkButton(frame_renovar, text="Renovar Contrato -",text_color="#00501B", width=40,
                                  height=30,cursor="hand2",command=self.ocultar_renovar,
                                    hover_color="#EEEEEE",fg_color=("#EEEEEE", "#1A1A1A"), font=("Impact", 16))
        self.renovar_menos.place(x=2, y=2)
        self.ocultar_ver_menos_renovar()

        self.renovar_mas = CTkButton(frame_renovar, text="Renovar Contrato +",text_color="#00501B", width=40,
                                  height=30,cursor="hand2",command=self.mostrar_renovar,
                                    hover_color="#EEEEEE",fg_color="#EEEEEE", font=("Impact", 16))
        self.renovar_mas.place(x=2, y=2)

        self.update_button = CTkButton(self.frame_botones_inferiores, text="Actualizar", fg_color="#00C853",
                                hover_color="#00E676", text_color="white",
                                font=("Ubuntu",13,"bold"), width=120, command=update)
        self.update_button.grid(row=0, column=0, padx=20, pady=5)


        self.limpiar = CTkButton(self.frame_botones_inferiores, text="Limpiar", fg_color="#FFA000",
                                hover_color="#FFB300", text_color="white",
                                font=("Ubuntu",13,"bold"), width=120, command=clear_entries)
        self.limpiar.grid(row=0, column=2, padx=20, pady=5)

        self.remove_one_button = CTkButton(self.frame_botones_inferiores,  text="Eliminar", fg_color="#D32F2F",
                                hover_color="#E53935", text_color="white",
                                font=("Ubuntu",13,"bold"), width=120, command=remove_one)
        self.remove_one_button.grid(row=0, column=3, padx=20, pady=5)



        self.ocultar_botones()


        em_entry.bind("<KeyRelease>", lambda e: mayusculas(e, em_entry))
        ff_entry.bind("<Button-1>", lambda e: abrir_calendario(e, ff_entry))
        self.my_tree.bind("<ButtonRelease-1>", select_record)
        
        get_current_date()
        query_db()


        self.root.mainloop()
    

    def actualizar_tree(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            port="3306",
            database="control_alquiler_Reych"
        )

        my_cursor = mydb.cursor()

        my_cursor.execute("""
            SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.nombre, c.telefono, r.CI, v.Placa, m.Nombre, o.Nombre FROM representante r INNER JOIN contratista c ON r.CI = c.Representante_CI INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON v.ID_Modelo = o.ID ORDER BY a.COD_Alquiler ASC; """)
        items = my_cursor.fetchall()

        for count, item in enumerate(items):
            tag = 'evenrow' if count % 2 == 0 else 'oddrow'
            self.my_tree.insert(parent='', index='end', iid=count, text='', values=item, tags=(tag,))

        mydb.close()



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
        self.frame_datos_detallados.actualizar_tree_datos()

    def ocultar_datos_detallados(self):
        self.frame_datos_detallados.pack_forget()
        self.tree_frame.pack(expand=True, fill=BOTH)
        self.ver()

    def mostrar_vehiculos_disponibles(self):
        self.frame_principal.pack_forget()
        self.frame_configuracion.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_estadisticas.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_vehiculos_disponibles.pack(expand=True, fill=BOTH)
        self.frame_vehiculos_disponibles.actualizar_tree_2()

    def mostrar_nuevo_vehiculo(self):
        self.frame_principal.pack_forget()
        self.frame_configuracion.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_estadisticas.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_nuevo_vehiculo.pack(expand=True, fill=BOTH)
        self.frame_nuevo_vehiculo.cargar_marcas()

    def mostrar_mantenimiento(self):
        self.frame_principal.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_configuracion.pack_forget()
        self.frame_estadisticas.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_mantenimeinto.pack(expand=True, fill=BOTH)

    def mostrar_configuracion(self):
        self.frame_mantenimeinto.pack_forget()
        self.frame_principal.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_estadisticas.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_configuracion.pack(expand=True, fill=BOTH)
        self.frame_configuracion.btn_backup.configure(state=DISABLED)

    def mostrar_estadisticas(self):
        self.frame_mantenimeinto.pack_forget()
        self.frame_principal.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_configuracion.pack_forget()
        self.frame_estadisticas.pack(expand=True, fill=BOTH)

    def mostrar_contenido_principal(self):
        self.frame_vehiculos_disponibles.pack_forget()
        self.frame_configuracion.pack_forget()
        self.frame_nuevo_vehiculo.pack_forget()
        self.frame_estadisticas.pack_forget()
        self.frame_mantenimeinto.pack_forget()
        self.frame_principal.pack(expand=True, fill=BOTH)
        self.actualizar_tree()
        

    def ocultar_botones(self):
        self.frame_botones_inferiores.pack_forget()

    def ocultar_entry(self):
        self.frame_contenedor_entry.pack_forget()

    def ocultar_renovar(self):
        self.frame_contenedor_entry.pack_forget()
        self.frame_botones_inferiores.pack_forget()
        self.data_frame.pack(side=TOP)
        self.ver_renovar()

    def mostrar_renovar(self):
        self.data_frame.pack_forget()
        self.frame_botones_inferiores.pack_forget()
        self.frame_contenedor_entry.pack(expand=True, fill=BOTH)
        self.no_ver_renovar()

    def ver_renovar(self):
        self.renovar_menos.place_forget()
        self.renovar_mas.place(x=10, y=2)

    def no_ver_renovar(self):
        self.renovar_mas.place_forget()
        self.renovar_menos.place(x=10, y=2)

    def mostrar_btn(self):
        self.frame_botones_inferiores.pack()

    def ocultar_ver_menos(self):
        self.ver_menos.place_forget()

    def ocultar_ver_menos_renovar(self):
        self.renovar_menos.place_forget()

    def ver(self):
        self.ver_menos.place_forget()
        self.ver_mas.place(x=10, y=2)

    def no_ver(self):
        self.ver_mas.place_forget()
        self.ver_menos.place(x=10, y=2)
