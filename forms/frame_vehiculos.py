from customtkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image
from forms.imprimir import imprimir_vehiculos
import os


class FrameVehiculos(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#EEEEEE")
        self.controlador = controlador

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123456",
            port = "3306",
            database = "control_alquiler_Reych"
        )

        my_cursor = mydb.cursor()

        def clear_entries_2():
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
            mostrar_imagen("default")

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

        
        def search_now():
                
                searched = self.buscar.get()
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


        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)

        titulo = CTkLabel(frame_superior, text="VEHICULOS",
                        text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        buscar_label_2 = CTkLabel(frame_superior, text="Buscar Vehículo:",
                                text_color="black", font=("Ubuntu", 15))
        buscar_label_2.pack(side="left", padx=15, pady=10)

        self.buscar = CTkEntry(frame_superior, width=250)
        self.buscar.pack(side="left", padx=5)

        searh = CTkButton(frame_superior, text="Buscar", font=("Ubuntu",13),
                               fg_color="#0E0F0F", text_color="white",
                               width=100, height=30, command=search_now)
        searh.pack(side="left", padx=10)


        img = Image.open("imagenes/imprimir.png")
        imprimir_icon = CTkImage(dark_image=img, light_image=img, size=(40,40))
        imprimir = CTkButton(frame_superior, hover_color="#EEEEEE" ,image=imprimir_icon , text="", fg_color="transparent",
                               width=30, height=30,command=imprimir_vehiculos)
        imprimir.pack(side="right", padx=3)


        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 5), pady=5)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                    selectmode="extended", show="headings")
        my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=my_tree.yview)


         #botones con las funciones
        frame_barra_derecha = CTkFrame(tabla_contenedor, fg_color="#000000", corner_radius=10)
        frame_barra_derecha.pack(side=RIGHT, fill=Y, padx=(5, 10), pady=5)

        self.img_label = CTkLabel(frame_barra_derecha, text="Imagen")
        self.img_label.pack(pady=30, padx=10)

        alquilar = CTkButton(frame_barra_derecha, text="Alquilar", fg_color="#00A86B", text_color="white",
                command=lambda:(ADD(), actualizar_tree_2()))
        alquilar.pack(pady=5)

        limpiar = CTkButton(frame_barra_derecha, text="Limpiar", fg_color="#D32F2F",text_color="white",command=clear_entries_2)
        limpiar.pack(pady=5)


        tree_scroll.config(command=my_tree.yview)


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
        my_tree.tag_configure('evenrow', background="#00A86B")

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
                background=[('selected',"#2c5c45")])
        
        def validate_entry(text,new_text):
            if len(new_text) > 11:#Hace que no supere los 10 digitos
                return False
            return text.isdecimal()
        
        def get_current_date():
            current_date = datetime.now().strftime('%d-%m-%Y')
            f1_entry.delete(0,END)
            f1_entry.insert(0, current_date)
            self.after(1000, get_current_date)
        
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

        # =================== Frame de datos ===================
        frame_inferior = CTkFrame(self, fg_color="#EEEEEE", corner_radius=10)
        frame_inferior.pack(padx=20, pady=10, fill="x")

        data_frame = CTkFrame(frame_inferior, fg_color="transparent")
        data_frame.pack(anchor="center")

        ci_label = CTkLabel(data_frame, text="C.I",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        ci_label.grid(row=0,column=0, padx=10,pady=10, sticky="ew")
        ci_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B",
                            validate="key",validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        ci_entry.grid(row=0,column=1,padx=10,pady=10) 

        r_name_label = CTkLabel(data_frame, text="Nombre",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        r_name_label.grid(row=0,column=2, padx=10,pady=10)
        r_name_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        r_name_entry.grid(row=0,column=3,padx=10,pady=10)

        apell_label = CTkLabel(data_frame, text="Apellido",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        apell_label.grid(row=0,column=4, padx=10,pady=10)
        apell_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        apell_entry.grid(row=0,column=5,padx=10,pady=10)

        J_label = CTkLabel(data_frame, text="RIF",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        J_label.grid(row=0,column=6, padx=10,pady=10)
        J_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B", validate="key",validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        J_entry.grid(row=0,column=7,padx=10,pady=10)

        e_name_label = CTkLabel(data_frame, text="Empresa",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        e_name_label.grid(row=1,column=0, padx=10,pady=10)
        e_name_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        e_name_entry.grid(row=1,column=1,padx=10,pady=10)

        dir_label = CTkLabel(data_frame, text="Direccion",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        dir_label.grid(row=1,column=2, padx=10,pady=10)
        dir_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        dir_entry.grid(row=1,column=3,padx=10,pady=10)

        cell_label = CTkLabel(data_frame, text="Teléfono",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        cell_label.grid(row=1,column=4, padx=10,pady=10)
        cell_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B", validate="key",
        validatecommand=(data_frame.register(validate_entry), "%S","%P"))
        cell_entry.grid(row=1,column=5,padx=10,pady=10)

        f1_label = CTkLabel(data_frame, text="Fecha I.",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        f1_label.grid(row=1,column=6, padx=10,pady=10)
        f1_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B",validate="key",
        validatecommand=(data_frame.register(get_current_date), "%P"))
        f1_entry.grid(row=1,column=7,padx=10,pady=10)

        f2_label = CTkLabel(data_frame, text="Fecha F.",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        f2_label.grid(row=2,column=0, padx=10,pady=10)
        f2_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B",validate="key",
        validatecommand=(data_frame.register(validate_fecha), "%P"))
        f2_entry.grid(row=2,column=1,padx=10,pady=10)

        plac_label = CTkLabel(data_frame, text="Placa",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        plac_label.grid(row=2,column=2, padx=10,pady=10)
        plac_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        plac_entry.grid(row=2,column=3,padx=10,pady=10)

        mar_label = CTkLabel(data_frame, text="Marca",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        mar_label.grid(row=2,column=4, padx=10,pady=10)
        mar_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        mar_entry.grid(row=2,column=5,padx=10,pady=10)

        modelo_label = CTkLabel(data_frame, text="Modelo",fg_color='transparent',text_color="black",
                        font=("Ubuntu",16))
        modelo_label.grid(row=2,column=6, padx=10,pady=10)
        modelo_entry = CTkEntry(data_frame,fg_color="#c2f1c1",text_color="black", border_color="#00501B")
        modelo_entry.grid(row=2,column=7,padx=10,pady=10)

        get_current_date()

        def ADD():

            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                port = "3306",
                database = "control_alquiler_Reych"
            )

            my_cursor = mydb.cursor()

            sql = "INSERT INTO representante (CI,nombre_r,apellido) VALUES (%s,%s,%s)"
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

            mostrar_imagen(values[1])

        def mostrar_imagen(placa):
            try:
                carpeta_imagenes = "imagenes_vehiculos"
                ruta_imagen = os.path.join(carpeta_imagenes, f"{placa}.jpg")

                if not os.path.exists(ruta_imagen):
                    ruta_imagen = os.path.join(carpeta_imagenes, "default.jpg")
                    if not os.path.exists(ruta_imagen):
                        self.img_label.configure(image=None, text="Sin imagen")
                        return

                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((200, 150))
                imagen_tk = CTkImage(light_image=imagen, dark_image=imagen, size=(200, 150))
                self.img_label.configure(image=imagen_tk, text="")
                self.img_label.image = imagen_tk

            except Exception as e:
                print("Error al cargar imagen:", e)
                self.img_label.configure(image=None, text="Error")

        mostrar_imagen("default")

        my_tree.bind("<ButtonRelease-1>", select_record)


        query_db()
