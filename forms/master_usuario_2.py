from tkinter import *
from tkinter import ttk
import tkinter as tk
import mysql.connector
from forms.imprimir_funcion import imprimir_vehiculos
from menu.empresa import detallado
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from datetime import datetime, timedelta
import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class usuario:
    def __init__(self):
        self.root = Tk()
        self.root.title('ALQUITECH')
        self.root.geometry("1250x520")
        self.root.config(background='#EEEEEE')

        barra_menu = Menu()
        menu_archivo = Menu(barra_menu,tearoff=False)
        menu_archivo.add_command(label='Ayuda', command=abrir_pdf)#, command=archico_nuevo
        #ventana.bind_all("<Control-n>",archico_nuevo)
        #menu_archivo.add_command(label="Datos detallados", command=atos)

        barra_menu.add_cascade(menu=menu_archivo, label='Menu')

        self.root.config(menu=barra_menu)

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
                background=[('selected',"#005954")])

        frame_form = Frame(self.root,bd=0,relief=SOLID,bg='#fcfcfc',height=50)
        frame_form.pack(side="top",expand=NO,fill=BOTH)

        frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='black')
        frame_form_top.pack(side="top",fill=X)
        

        frame_form_left = CTkFrame(self.root,fg_color='transparent',height=50)
        frame_form_left.pack(side="left",expand=NO,fill=BOTH)#, pady=20

        frame_form_l = CTkFrame(frame_form_left,fg_color='#005954', width=200, #corner_radius=20,
                                border_color="lightgreen", border_width=4)
        frame_form_l.pack(side="left",fill=Y)

        frame_top = CTkFrame(frame_form_l, fg_color="transparent")
        frame_top.pack(side="top",fill=X, pady=15)

        title = CTkLabel(master=frame_top,text="Alquitech",font=('YRSA SEMIBOLD',40),text_color="white",fg_color='#005954',pady=1)#008259  ff8c69
        title.pack(expand=YES,fill=BOTH, pady=5, padx=15)

        frame_top2 = CTkFrame(frame_top, fg_color="transparent", height=80)
        frame_top2.pack(side="top",fill=X)

        logo_path = get_project_root() / "imagenes" / "logoapp.png"
        imglogo = Image.open(logo_path)

        logo_frame = CTkFrame(frame_top2,fg_color="transparent",width=50, height=50)
        logo_frame.pack(side="top",fill=X, padx=5)

        bg = CTkLabel(master=logo_frame, text=None,image=CTkImage(dark_image=imglogo, light_image=imglogo, size=(100,100)))
        bg.pack(anchor="center", padx=30)

        frame_botones = CTkFrame(frame_form_l, fg_color="transparent")
        frame_botones.pack(side="top",fill=X, pady=20)

        date_detalles = CTkButton(frame_botones, text="Datos detallados",fg_color="transparent",text_color="white",
                                  width=150, height=40,
                                  font=("Ubuntu",18), command=detallado)
        date_detalles.pack(pady=5, padx=2)

        #imprimir = CTkButton(frame_botones, text="Exportar datos",fg_color="transparent", command=select_imprimir,text_color="white",
        #                          width=150, height=40,
        #                          font=("Ubuntu",18))
        #imprimir.pack(pady=5, padx=2)

        def romper():
            self.root.destroy()

            from forms.form_login import App

            App()

            

        frame_botones2 = CTkFrame(frame_form_l, fg_color="transparent")
        frame_botones2.pack(side="bottom",fill=X, pady=20)

        boton = CTkButton(frame_botones2, text="Cerrar Sesión",fg_color="transparent", text_color="white",
                                  width=100, height=30,
                                  font=("Ubuntu",18), command=romper)
        boton.pack(pady=5, padx=2, side="left")


        

        ######################## BOTONES ################################
        button_frame = CTkFrame(self.root, fg_color="transparent")
        button_frame.pack(expand=NO,padx=20)

        def actualizar_tree():
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

            my_cursor.execute("SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.Nombre, c.telefono, v.Placa, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID;")
            items = my_cursor.fetchall()

            count = 0

            for item in items:
                if count % 2 == 0:
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]),tags=('evenrow',))
                else: 
                    my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]),tags=('oddrow',))

                count += 1

            conn.commit()
            conn.close()

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
                sql = "SELECT a.COD_Alquiler, a.Fecha, a.Fecha_Expiracion, c.RIF, c.Nombre, c.telefono, v.Placa, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID WHERE COD_Alquiler = {0}"

                my_cursor.execute(sql.format(buscar.get()))
                records = my_cursor.fetchall()
                
                
                for record in records:
                                my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8]))#,


                conn.commit()
                conn.close()

        busqueda = CTkFrame(self.root, fg_color="transparent")
        busqueda.pack(pady=2)

        buscar = CTkEntry(busqueda, placeholder_text="Ingrese codigo de alquiler", placeholder_text_color="white",width=200, height=35,text_color="black",
                           fg_color="#005954", border_color="lightgreen")
        buscar.grid(row=0, column=0,pady=5)

        searh = CTkButton(busqueda, text="Buscar",fg_color="#005954", text_color="white",
                                  width=100, height=35,border_color="lightgreen",border_width=2,
                                  font=("Ubuntu",18), command=search_now)
        searh.grid(row=0, column=1, padx=5)


        tree_frame = CTkFrame(self.root, corner_radius=20)
        tree_frame.pack(pady=20)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT,fill=Y)


        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",show="headings")
        my_tree.pack()

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
        my_tree.heading("FechaI", text="Fecha I.",anchor=CENTER)
        my_tree.heading("FechaF", text="Fecha F.",anchor=CENTER)
        my_tree.heading("RIF", text="RIF",anchor=CENTER)
        my_tree.heading("Empresa", text="Empresa",anchor=CENTER)
        my_tree.heading("TLF", text="Teléfono",anchor=CENTER)
        my_tree.heading("CI", text="C.I",anchor=CENTER)
        my_tree.heading("Placa", text="Placa",anchor=CENTER)
        my_tree.heading("Modelo", text="Vehículo Modelo",anchor=CENTER)
        my_tree.heading("Marca", text="Vehículo Marca",anchor=CENTER)

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#5dc1b9")

        #ENTRYS

        #VALIDACION DE LOS ENTRYS


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
        
        
        data_frame = CTkFrame(self.root,corner_radius=10,fg_color="transparent")#d5ffff
        data_frame.pack(fill="x", expand=YES, padx=70)

        COD_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=100, height=20)
        COD_frame.grid(row=1, column=4, padx=25,pady=4, ipady=3)

        COD_label = CTkLabel(COD_frame, text="Cod.",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        COD_label.grid(row=0, column=0, padx=10, pady=1)
        COD_entry = CTkEntry(COD_frame,justify=CENTER,width=130,fg_color="transparent",text_color="black", border_color="#005954",
                             validate="key", validatecommand=(data_frame.register(validate_entry2), "%S","%P"))
        COD_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha1_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=100, height=20)
        fecha1_frame.grid(row=0, column=0,padx=25,pady=4, ipady=3)

        fi_label = CTkLabel(fecha1_frame, text="Fecha Inicial",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        fi_label.grid(row=0,column=0, padx=10, pady=1)
        fi_entry = CTkEntry(fecha1_frame,justify=CENTER,fg_color="transparent",text_color="black", width=130, border_color="#005954",
                            validate="key", validatecommand=(data_frame.register(validate_fecha), "%P"))
        fi_entry.grid(row=1,column=0, padx=10, pady=1)

        fecha2_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        fecha2_frame.grid(row=0, column=1,padx=25,pady=4, ipady=3)

        ff_label = CTkLabel(fecha2_frame, text="Fecha Final",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        ff_label.grid(row=0,column=0, padx=10, pady=1)
        ff_entry = CTkEntry(fecha2_frame, justify=CENTER,fg_color="transparent",text_color="black", width=130, border_color="#005954",
                            validate="key", validatecommand=(data_frame.register(validate_fecha), "%P"))
        ff_entry.grid(row=1,column=0, padx=10, pady=1)

        rif_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6,  width=50, height=20,)
        rif_frame.grid(row=0, column=2,padx=25,pady=4, ipady=3)

        rif_label = CTkLabel(rif_frame, text="RIF",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        rif_label.grid(row=0,column=0, padx=10, pady=1)
        rif_entry = CTkEntry(rif_frame, justify=CENTER,fg_color="transparent", text_color="black", width=130,  border_color="#005954",
                             validate="key", validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        rif_entry.grid(row=1,column=0, padx=10, pady=1)

        empresa_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=35, height=20,)
        empresa_frame.grid(row=0, column=3,padx=25,pady=4, ipady=3)

        em_label = CTkLabel(empresa_frame, text="Empresa",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        em_label.grid(row=0,column=0, padx=10, pady=1)
        em_entry = CTkEntry(empresa_frame, justify=CENTER,fg_color="transparent",text_color="black", border_color="#005954",
                            width=130)
        em_entry.grid(row=1,column=0, padx=10, pady=1)
        
        ci_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20)
        ci_frame.grid(row=0, column=4, padx=25,pady=4, ipady=3)

        ci_label = CTkLabel(ci_frame, text="C.I",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        ci_label.grid(row=0, column=0, padx=10, pady=1)
        ci_entry = CTkEntry(ci_frame,justify=CENTER,width=130,fg_color="transparent",text_color="black", border_color="#005954",
                             validate="key", validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        ci_entry.grid(row=1,column=0, padx=10, pady=1)

        tlf_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        tlf_frame.grid(row=1, column=0,padx=25,pady=4, ipady=3)

        tlf_label = CTkLabel(tlf_frame, text="Tfno",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        tlf_label.grid(row=0,column=0, padx=10, pady=1)
        tlf_entry = CTkEntry(tlf_frame,justify=CENTER, fg_color="transparent",text_color="black", width=130, border_color="#005954",
                             validate="key", validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        tlf_entry.grid(row=1,column=0, padx=10, pady=1)

        placa_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        placa_frame.grid(row=1, column=1,padx=10,pady=4, ipady=3)

        placa_label = CTkLabel(placa_frame, text="Placa",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        placa_label.grid(row=0,column=0, padx=10, pady=1)
        placa_entry = CTkEntry(placa_frame, justify=CENTER,fg_color="transparent", text_color="black", width=130, border_color="#005954",)
        placa_entry.grid(row=1,column=0, padx=10, pady=1)

        marca_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        marca_frame.grid(row=1, column=2,padx=10,pady=4, ipady=3)

        marca_label = CTkLabel(marca_frame, text="Marca",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        marca_label.grid(row=0,column=0, padx=10, pady=1)
        marca_entry = CTkEntry(marca_frame, justify=CENTER,fg_color="transparent", text_color="black",width=130, border_color="#005954",)
        marca_entry.grid(row=1,column=0, padx=10, pady=1)

        model_frame = CTkFrame(data_frame, fg_color="transparent",corner_radius=6, width=50, height=20,)
        model_frame.grid(row=1, column=3,padx=10,pady=4, ipady=3)

        model_label = CTkLabel(model_frame, text="Modelo",fg_color="transparent",text_color="#005954",
                                    font=("Ubuntu",16))
        model_label.grid(row=0,column=0, padx=10, pady=1)
        model_entry = CTkEntry(model_frame,justify=CENTER, fg_color="transparent", text_color="black",width=130, border_color="#005954",)
        model_entry.grid(row=1,column=0, padx=10, pady=1)

        
        #FUNCIONES
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
                titulo = 'Alquilado'
                mensaje = 'Ocurrio un problema'
                messagebox.showinfo(titulo, mensaje)
            finally:
                actualizar_tree()

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

        def select_record(e):
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

            selected = my_tree.focus()
            values = my_tree.item(selected,'values')

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
                titulo = 'Alquilado'
                mensaje = 'Ocurrio un problema'
                messagebox.showinfo(titulo, mensaje)
            finally:
                actualizar_tree()

            

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

        def abrir():
            #self.root.destroy()
        
            class usuario2:
                def __init__(self):
                    self.root = tk.Toplevel()
                    self.root.title('VENTANA 2')
                    self.root.geometry("1250x520")
                    self.root.config(background='#EEEEEE')                                  #NARANJA

                    barra_menu = Menu()
                    menu_archivo = Menu(barra_menu,tearoff=False)
                    menu_archivo.add_command(label='Ayuda',accelerator='Ctrl+N')#, command=archico_nuevo
                    #ventana.bind_all("<Control-n>",archico_nuevo)
                    #menu_archivo.add_command(label="Clientes registrados")

                    barra_menu.add_cascade(menu=menu_archivo, label='Menu')

                    self.root.config(menu=barra_menu)

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

                        my_cursor.execute("SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca ORDER BY a.COD_Alquiler ASC;")
                        records = my_cursor.fetchall()

                        count = 0

                        for record in records:
                            if count % 2 == 0:
                                my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',))
                            else: 
                                my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',))

                            count += 1

                        conn.commit()
                        conn.close()


                    style = ttk.Style()

                    style.theme_use('clam')

                    style.configure(
                        "Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white"
                    )

                    style.map('Treeview',
                            background=[('selected',"#57bd9e")])
                    
                    frame_form = Frame(self.root,bd=0,relief=SOLID,bg='#fcfcfc',height=50)
                    frame_form.pack(side="top",expand=NO,fill=BOTH)

                    frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='black')
                    frame_form_top.pack(side="top",fill=X)
                    

                    frame_form_left = CTkFrame(self.root,fg_color='transparent',height=50)
                    frame_form_left.pack(side="left",expand=NO,fill=BOTH)#, pady=20

                    frame_form_l = CTkFrame(frame_form_left,fg_color='#005954', width=200, #corner_radius=20,
                                            border_color="lightgreen", border_width=4)
                    frame_form_l.pack(side="left",fill=Y)

                    frame_top = CTkFrame(frame_form_l, fg_color="transparent")
                    frame_top.pack(side="top",fill=X, pady=15)

                    title = CTkLabel(master=frame_top,text="Alquitech",font=('YRSA SEMIBOLD',40),text_color="white",fg_color='transparent',pady=1)#008259  ff8c69
                    title.pack(expand=YES,fill=BOTH, pady=5, padx=15)

                    frame_top2 = CTkFrame(frame_top, fg_color="transparent", height=80)
                    frame_top2.pack(side="top",fill=X)

                    imglogo = Image.open(logo_path)

                    logo_frame = CTkFrame(frame_top2,fg_color="transparent",width=50, height=50)
                    logo_frame.pack(side="top",fill=X, padx=5)

                    bg = CTkLabel(master=logo_frame, text=None,image=CTkImage(dark_image=imglogo, light_image=imglogo, size=(100,100)))
                    bg.pack(anchor="center", padx=30)

                    frame_botones = CTkFrame(frame_form_l, fg_color="transparent")
                    frame_botones.pack(side="top",fill=X, pady=20)

                    imprimir = CTkButton(frame_botones, text="Exportar datos",fg_color="transparent", command=imprimir_vehiculos,text_color="white",
                                            width=150, height=40,
                                            font=("Ubuntu",18))
                    imprimir.pack(pady=5, padx=2)



                    #vole = CTkButton(frame_botones, text="Volver",fg_color="transparent",text_color="white",
                    #                        width=150, height=40,
                    #                        font=("Ubuntu",18))
                    #vole.pack(pady=5, padx=2)

                    def romper():
                        self.root.destroy()
                        
                        from forms.form_login import App

                        App()

                    frame_botones2 = CTkFrame(frame_form_l, fg_color="transparent")
                    frame_botones2.pack(side="bottom",fill=X, pady=20)

                    #boton = CTkButton(frame_botones2, text="Cerrar Sesión",fg_color="transparent", text_color="white",
                    #                        width=100, height=30,
                    #                        font=("Ubuntu",18), command=romper)
                    #boton.pack(pady=5, padx=2, side="left")


                    ######################## BOTONES ################################
                    button_frame = CTkFrame(self.root, fg_color="transparent")
                    button_frame.pack(expand=NO,padx=20)

                    def search_now():
                            
                            searched = buscar.get()
                            name = (searched, )
                            
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
                            sql = "SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca WHERE m.Nombre = %s ORDER BY a.COD_Alquiler ASC;"

                            my_cursor.execute(sql,name)
                            records = my_cursor.fetchall()
                            
                            count = 0
                            for record in records:
                                    if count % 2 == 0:
                                        my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',))#,
                                    else:
                                        my_tree.insert(parent='',index='end',text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',))#,
                                    count +=1

                            conn.commit()
                            conn.close()

                    def actualizar_tree():
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

                        my_cursor.execute("SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca ORDER BY a.COD_Alquiler ASC;")
                        items = my_cursor.fetchall()

                        count = 0

                        for item in items:
                            if count % 2 == 0:
                                my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3]),tags=('evenrow',))
                            else: 
                                my_tree.insert(parent='',index='end',iid=count,text='',values=(item[0],item[1],item[2],item[3]),tags=('oddrow',))

                            count += 1

                        conn.commit()
                        conn.close()

                    busqueda = CTkFrame(self.root, fg_color="transparent")
                    busqueda.pack()

                    buscar = CTkEntry(busqueda, placeholder_text="Ingrese marca del vehiculo", placeholder_text_color="white",width=200, height=35,text_color="white",
                                    fg_color="#005954", border_color="lightgreen")
                    buscar.grid(row=0, column=0,pady=10)

                    searh = CTkButton(busqueda, text="Buscar",fg_color="#005954", text_color="white",
                                            width=100, height=35,border_color="lightgreen",border_width=2,
                                            font=("Ubuntu",18), command=search_now)
                    searh.grid(row=0, column=1, padx=5)
                    
                    refresh = CTkButton(busqueda, text="Refresh",fg_color="#005954", text_color="white",
                                            width=100, height=35,border_color="lightgreen",border_width=2,
                                            font=("Ubuntu",18), command=actualizar_tree)
                    refresh.grid(row=0, column=2, padx=5)

                    tree_frame = Frame(self.root)
                    tree_frame.pack(pady=10)

                    tree_scroll = Scrollbar(tree_frame)
                    tree_scroll.pack(side=RIGHT,fill=Y)

                    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",show="headings")
                    my_tree.pack()

                    tree_scroll.config(command=my_tree.yview)

                    #CREACION DE COLUMNAS
                    my_tree['columns']=("COD","Placa","Marca","Modelo")

                    my_tree.column("COD",anchor=CENTER,width=140)
                    my_tree.column("Placa",anchor=CENTER,width=140)
                    my_tree.column("Marca",anchor=CENTER,width=140)
                    my_tree.column("Modelo",anchor=CENTER,width=140)


                    my_tree.heading("COD", text="COD Alquiler",anchor=CENTER)
                    my_tree.heading("Placa", text="Placa",anchor=CENTER)
                    my_tree.heading("Marca", text="Vehículo Marca",anchor=CENTER)
                    my_tree.heading("Modelo", text="Vehículo Modelo",anchor=CENTER)
                    

                    my_tree.tag_configure('oddrow', background="white")
                    my_tree.tag_configure('evenrow', background="#5dc1b9")

                    #ENTRYS

                    #VALIDACION DE LOS ENTRYS
                    def validate_entry(text,new_text):
                        if len(new_text) > 11:#Hace que no supere los 10 digitos
                            return False
                        return text.isdecimal()
                    
                    def get_current_date():
                        current_date = datetime.now().strftime('%d-%m-%Y')
                        f1_entry.delete(0,END)
                        f1_entry.insert(0, current_date)
                        self.root.after(1000, get_current_date)
                    
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
                        
                        

                    data_frame = CTkFrame(self.root, corner_radius=10,fg_color="#005954", border_color="lightgreen", border_width=2)#d5ffff
                    data_frame.pack(fill="x", expand=YES, padx=20)

                    ci_label = CTkLabel(data_frame, text="C.I",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    ci_label.grid(row=0,column=0, padx=10,pady=10)
                    ci_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1",
                                        validate="key",validatecommand=(data_frame.register(validate_entry), "%S","%P"))
                    ci_entry.grid(row=0,column=1,padx=10,pady=10) 

                    r_name_label = CTkLabel(data_frame, text="Nombre",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    r_name_label.grid(row=0,column=2, padx=10,pady=10)
                    r_name_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    r_name_entry.grid(row=0,column=3,padx=10,pady=10)

                    apell_label = CTkLabel(data_frame, text="Apellido",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    apell_label.grid(row=0,column=4, padx=10,pady=10)
                    apell_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    apell_entry.grid(row=0,column=5,padx=10,pady=10)

                    J_label = CTkLabel(data_frame, text="RIF",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    J_label.grid(row=0,column=6, padx=10,pady=10)
                    J_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1", validate="key",validatecommand=(data_frame.register(validate_entry), "%S","%P"))
                    J_entry.grid(row=0,column=7,padx=10,pady=10)

                    e_name_label = CTkLabel(data_frame, text="Empresa",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    e_name_label.grid(row=1,column=0, padx=10,pady=10)
                    e_name_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    e_name_entry.grid(row=1,column=1,padx=10,pady=10)

                    dir_label = CTkLabel(data_frame, text="Direccion",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    dir_label.grid(row=1,column=2, padx=10,pady=10)
                    dir_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    dir_entry.grid(row=1,column=3,padx=10,pady=10)

                    cell_label = CTkLabel(data_frame, text="Teléfono",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    cell_label.grid(row=1,column=4, padx=10,pady=10)
                    cell_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1", validate="key",
                    validatecommand=(data_frame.register(validate_entry), "%S","%P"))
                    cell_entry.grid(row=1,column=5,padx=10,pady=10)

                    f1_label = CTkLabel(data_frame, text="Fecha I.",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    f1_label.grid(row=1,column=6, padx=10,pady=10)
                    f1_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1",validate="key",
                    validatecommand=(data_frame.register(get_current_date), "%P"))
                    f1_entry.grid(row=1,column=7,padx=10,pady=10)

                    f2_label = CTkLabel(data_frame, text="Fecha F.",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    f2_label.grid(row=2,column=0, padx=10,pady=10)
                    f2_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1",validate="key",
                    validatecommand=(data_frame.register(validate_fecha), "%P"))
                    f2_entry.grid(row=2,column=1,padx=10,pady=10)

                    plac_label = CTkLabel(data_frame, text="Placa",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    plac_label.grid(row=2,column=2, padx=10,pady=10)
                    plac_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    plac_entry.grid(row=2,column=3,padx=10,pady=10)

                    mar_label = CTkLabel(data_frame, text="Marca",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    mar_label.grid(row=2,column=4, padx=10,pady=10)
                    mar_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    mar_entry.grid(row=2,column=5,padx=10,pady=10)

                    modelo_label = CTkLabel(data_frame, text="Modelo",fg_color='transparent',text_color="white",
                                    font=("Ubuntu",16))
                    modelo_label.grid(row=2,column=6, padx=10,pady=10)
                    modelo_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#c2f1c1")
                    modelo_entry.grid(row=2,column=7,padx=10,pady=10)
                    
                    get_current_date()
                    

                    #FUNCIONES
                    def ADD():

                        mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "123456",
                            port = "3306",
                            database = "control_alquiler_Reych"
                        )

                        my_cursor = mydb.cursor()

                        sql = "INSERT INTO representante (CI,nombre,apellido) VALUES (%s,%s,%s)"
                        values = (ci_entry.get(),r_name_entry.get(),apell_entry.get())
                        #my_cursor.execute(sql,values)
                        #mydb.commit()
                        sql2 = "INSERT INTO contratista (RIF, nombre, direccion, telefono, Representante_CI) VALUES (%s,%s,%s,%s,%s)"
                        values2 = (J_entry.get(),e_name_entry.get(),dir_entry.get(),cell_entry.get(),ci_entry.get())
                        #my_cursor.execute(sql2,values2)
                        #mydb.commit()
                        sql3 = "INSERT INTO alquiler (Fecha, RIF_Empresa, Placa_Vehiculo, Fecha_Expiracion) VALUES (%s,%s,%s,%s)"
                        values3 = (f1_entry.get(),J_entry.get(),plac_entry.get(),f2_entry.get())
                        #my_cursor.execute(sql3,values3)
                        #mydb.commit()
                        try:
                            my_cursor.execute(sql,values)
                            mydb.commit()
                            #conn.close()
                            my_cursor.execute(sql2,values2)
                            mydb.commit()
                            #conn.close()
                            my_cursor.execute(sql3,values3)
                            mydb.commit()
                            titulo = 'Alquilado'
                            mensaje = 'Vehiculo alquilado con exito'
                            messagebox.showinfo(titulo, mensaje)
                        except:
                            titulo = 'Alquilado'
                            mensaje = 'Ocurrio un problema'
                            messagebox.showinfo(titulo, mensaje)

                        f1_entry.delete(0,END)
                        f2_entry.delete(0,END)
                        ci_entry.delete(0,END)
                        r_name_entry.delete(0,END)
                        apell_entry.delete(0,END)
                        J_entry.delete(0,END)
                        e_name_entry.delete(0,END)
                        dir_entry.delete(0,END)
                        cell_entry.delete(0,END)
                        plac_entry.delete(0,END)
                        mar_entry.delete(0,END)
                        modelo_entry.delete(0,END)

                    def clear_entries():
                        f1_entry.delete(0,END)
                        f2_entry.delete(0,END)
                        ci_entry.delete(0,END)
                        r_name_entry.delete(0,END)
                        apell_entry.delete(0,END)
                        J_entry.delete(0,END)
                        e_name_entry.delete(0,END)
                        dir_entry.delete(0,END)
                        cell_entry.delete(0,END)
                        plac_entry.delete(0,END)
                        mar_entry.delete(0,END)
                        modelo_entry.delete(0,END)

                    def select_record(e):#Esta funcion estaba comentanda
                        f1_entry.delete(0,END)
                        f2_entry.delete(0,END)
                        ci_entry.delete(0,END)
                        r_name_entry.delete(0,END)
                        apell_entry.delete(0,END)
                        J_entry.delete(0,END)
                        e_name_entry.delete(0,END)
                        dir_entry.delete(0,END)
                        cell_entry.delete(0,END)
                        plac_entry.delete(0,END)
                        mar_entry.delete(0,END)
                        modelo_entry.delete(0,END)

                        selected = my_tree.focus()
                        values = my_tree.item(selected,'values')

                        plac_entry.insert(0,values[1])
                        mar_entry.insert(0,values[2])
                        modelo_entry.insert(0,values[3])

                    '''def back():
                       self.root.destroy()

                       usuario()'''
                                


                    #BOTONES

                    limpiar_path = get_project_root() / "imagenes" / "limpiar.png"
                    add_path = get_project_root() / "imagenes" / "add.png"
                    limpiar = Image.open(limpiar_path)
                    added = Image.open(add_path)

                    add_button = CTkButton(button_frame,text="Agregar",command=ADD,corner_radius=15, 
                                           text_color="white",width=200,height=50,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="#005954",hover_color="#5acf59", font=("Impact", 20),
                                        image=CTkImage(dark_image=added,light_image=added))
                    add_button.grid(row=1,column=1,padx=20,pady=10)
                    
                    insertar_vehiculos = CTkButton(button_frame,text="Insertar Vehiculos",corner_radius=15, 
                                           text_color="white",width=200,height=50,cursor='hand2',
                                           border_color="lightgreen",border_width=2, state=DISABLED,
                                        fg_color="#005954",hover_color="#5acf59", font=("Impact", 20),
                                        image=CTkImage(dark_image=added,light_image=added))
                    insertar_vehiculos.grid(row=1,column=2,padx=20,pady=10)

                    select_record_button = CTkButton(button_frame,text="Limpiar",command=clear_entries,corner_radius=15, 
                                           text_color="white",width=200,height=50,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="#005954",hover_color="#5acf59", font=("Impact", 20),
                                        image=CTkImage(dark_image=limpiar,light_image=limpiar))
                    select_record_button.grid(row=1,column=7,padx=20,pady=10)

                    my_tree.bind("<ButtonRelease-1>", select_record)

                    query_db()
                    self.root.mainloop()
            usuario2()


        actu_path = get_project_root() / "imagenes" / "update.png"
        dele_path = get_project_root() / "imagenes" / "eliminar.png"
        selet_path = get_project_root() / "imagenes" / "limpiar.png"
        rent_path = get_project_root() / "imagenes" / "rentarbox.png"
        actu = Image.open(actu_path)
        dele = Image.open(dele_path)
        selet = Image.open(selet_path)
        rent = Image.open(rent_path)

        update_button = CTkButton(button_frame,text="Actualizar",command=update,corner_radius=15, state=DISABLED,text_color="white",width=200,height=50,cursor='hand2',
                             fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20),
                             border_color="lightgreen",border_width=2,
                             image=CTkImage(dark_image=actu,light_image=actu))
        update_button.grid(row=1,column=0,padx=30,pady=20)

        remove_one_button = CTkButton(button_frame,text="Eliminar",corner_radius=15, state=DISABLED,command=remove_one,text_color="white",width=200,height=50,cursor='hand2',
                             fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20),
                             border_color="lightgreen",border_width=2,
                             image=CTkImage(dark_image=dele,light_image=dele))#2ca880
        remove_one_button.grid(row=1,column=3,padx=30,pady=20)

        select_record_button = CTkButton(button_frame,text="Limpiar",corner_radius=15,command=clear_entries,text_color="white",width=200,height=50,cursor='hand2',
                             fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20),
                             border_color="lightgreen",border_width=2,
                             image=CTkImage(dark_image=selet,light_image=selet))#00986c
        select_record_button.grid(row=1,column=7,padx=30,pady=20)

        open_window = CTkButton(button_frame,text="Alquilar", command=abrir, corner_radius=15,text_color="white",width=200,height=50,cursor='hand2',
                             fg_color="#005954",hover_color="#57bd9e", font=("Impact", 20),
                             border_color="lightgreen",border_width=2,
                             image=CTkImage(dark_image=rent,light_image=rent))#008d62
        open_window.grid(row=1,column=8,padx=30,pady=20)

        my_tree.bind("<ButtonRelease-1>", select_record)

        query_db()


        self.root.mainloop()
    
            
def abrir_pdf():
    if os.path.exists(ruta_pdf):
        os.system(f'start {ruta_pdf}')
        
pdf_path = get_project_root() / "PDF" / "manual.pdf"        
ruta_pdf = pdf_path