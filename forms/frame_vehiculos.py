from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import tkinter as tk
import mysql.connector
from PIL import Image
from forms.imprimir_funcion import imprimir_vehiculos
from tkcalendar import Calendar
from datetime import date
import os


class FrameVehiculos(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=("#EEEEEE", "#1A1A1A"))
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
            # Limpiar nuevos campos
            ci_num_entry.delete(0, END)
            ci_prefix_menu.set("V")
            rif_num_entry.delete(0, END)
            rif_prefix_menu.set("V")
            tlf_num_entry.delete(0, END)
            tlf_prefix_menu.set("0414")
            
            r_name_entry.delete(0,END)
            apell_entry.delete(0,END)
            e_name_entry.delete(0,END)
            dir_entry.delete(0,END)
            plac_entry.delete(0,END)
            mar_entry.delete(0,END)
            modelo_entry.delete(0,END)
            mostrar_imagen("default")


        def query_db():
                conn = mydb

                my_cursor = mydb.cursor()

                my_cursor.execute("SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON v.ID_Modelo = o.ID WHERE a.COD_Alquiler IS NULL ORDER BY a.COD_Alquiler ASC;")
                records = my_cursor.fetchall()

                count = 0

                for record in records:
                    if count % 2 == 0:
                        self.my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',))
                    else: 
                        self.my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',))

                    count += 1

                conn.commit()
                conn.close()

        def ADD():
            try:
                mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "123456",
                    port = "3306",
                    database = "control_alquiler_Reych"
                )
                my_cursor = mydb.cursor()

                ci_val = f"{ci_prefix_menu.get()}-{ci_num_entry.get().strip()}"
                nombre_val = r_name_entry.get().strip()
                apellido_val = apell_entry.get().strip()
                rif_val = f"{rif_prefix_menu.get()}-{rif_num_entry.get().strip()}"
                empresa_val = e_name_entry.get().strip()
                direccion_val = dir_entry.get().strip()
                telefono_val = f"{tlf_prefix_menu.get()}-{tlf_num_entry.get().strip()}"
                placa_val = plac_entry.get().strip()
                fecha_inicio = f1_entry.get().strip()
                fecha_fin = f2_entry.get().strip()

                try:
                    if fecha_inicio:
                        d = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                        fecha_inicio_sql = d.strftime("%Y-%m-%d")
                    else:
                        fecha_inicio_sql = None

                    if fecha_fin:
                        d2 = datetime.strptime(fecha_fin, "%d-%m-%Y")
                        fecha_fin_sql = d2.strftime("%Y-%m-%d")
                    else:
                        fecha_fin_sql = None
                except Exception:
                    fecha_inicio_sql = fecha_inicio
                    fecha_fin_sql = fecha_fin

 
                def existe_tabla(campo, valor, tabla, columna):
                    sql_check = f"SELECT 1 FROM {tabla} WHERE {columna} = %s LIMIT 1"
                    my_cursor.execute(sql_check, (valor,))
                    return my_cursor.fetchone() is not None

                if ci_val:
                    if not existe_tabla("CI", ci_val, "representante", "CI"):
                        sql = "INSERT INTO representante (CI, nombre, apellido) VALUES (%s, %s, %s)"
                        my_cursor.execute(sql, (ci_val, nombre_val, apellido_val))
                        mydb.commit()
                else:
                    raise ValueError("El campo C.I. está vacío.")

                if rif_val:
                    if not existe_tabla("RIF", rif_val, "contratista", "RIF"):
                        sql2 = "INSERT INTO contratista (RIF, nombre, direccion, telefono, Representante_CI) VALUES (%s, %s, %s, %s, %s)"
                        my_cursor.execute(sql2, (rif_val, empresa_val, direccion_val, telefono_val, ci_val))
                        mydb.commit()
                    else:
                        pass
                else:
                    raise ValueError("El campo RIF está vacío.")

                # Calcular el siguiente COD_Alquiler manualmente para asegurar continuidad
                my_cursor.execute("SELECT IFNULL(MAX(COD_Alquiler), 0) + 1 FROM alquiler")
                next_id = my_cursor.fetchone()[0]

                sql3 = "INSERT INTO alquiler (COD_Alquiler, Fecha, RIF_Empresa, Placa_Vehiculo, Fecha_Expiracion) VALUES (%s, %s, %s, %s, %s)"
                my_cursor.execute(sql3, (next_id, fecha_inicio_sql, rif_val, placa_val, fecha_fin_sql))
                mydb.commit()

                messagebox.showinfo("Alquilado", "Vehiculo alquilado con éxito")
            except Exception as e:
                print("Error en ADD():", repr(e))
                messagebox.showerror("Error al alquilar", f"Ocurrió un problema:\n{e}")
            finally:
                self.actualizar_tree_2()
                clear_entries_2()
                try:
                    my_cursor.close()
                except:
                    pass
                try:
                    mydb.close()
                except:
                    pass


        def search_now(event=None):
                
                searched = self.buscar.get()
                
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

                if not searched.strip():
                    sql = """SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre 
                             FROM vehiculo v 
                             LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa 
                             RIGHT JOIN marca m ON m.ID = v.ID_Marca 
                             INNER JOIN modelo o ON v.ID_Modelo = o.ID 
                             WHERE a.COD_Alquiler IS NULL 
                             ORDER BY m.Nombre ASC;"""
                    my_cursor.execute(sql)
                else:
                    like_pattern = f"%{searched}%"
                    sql = """SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre 
                             FROM vehiculo v 
                             LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa 
                             RIGHT JOIN marca m ON m.ID = v.ID_Marca 
                             INNER JOIN modelo o ON v.ID_Modelo = o.ID 
                             WHERE (m.Nombre LIKE %s OR o.Nombre LIKE %s) 
                             AND a.COD_Alquiler IS NULL 
                             ORDER BY m.Nombre ASC;"""
                    my_cursor.execute(sql, (like_pattern, like_pattern))

                records = my_cursor.fetchall()
                
                for count, record in enumerate(records):
                    tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                    self.my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=(tag,))

                conn.commit()
                conn.close()
                


        frame_superior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))
        frame_superior.pack(pady=10, fill=X, expand=True)

        titulo = CTkLabel(frame_superior, text="VEHÍCULOS",
                        text_color=("#00501B", "#00FF7F"), font=("Impact", 45))

        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        buscar_label_2 = CTkLabel(frame_superior, text="Buscar:",
                                text_color=("black", "white"), font=("Ubuntu", 15,"bold"))
        buscar_label_2.pack(side="left", padx=5, pady=10)

        self.buscar = CTkEntry(frame_superior, fg_color=("#c2f1c1", "#2D2D2D"),border_color="#00501B",width=250)
        self.buscar.pack(side="left", padx=5)
        self.buscar.bind("<KeyRelease>", search_now)


        img = Image.open("imagenes/imprimir.png")
        img_white = Image.open("imagenes/imprimir_white.png")
        imprimir_icon = CTkImage(light_image=img, dark_image=img_white, size=(40,40))

        imprimir = CTkButton(frame_superior, hover_color=("#EEEEEE", "#2D2D2D") ,image=imprimir_icon , text="", fg_color="transparent",

                               width=30, height=30, command=lambda: imprimir_vehiculos(self.controlador.tipo_usuario))
        imprimir.pack(side="right", padx=3)


        tabla_contenedor = CTkFrame(self, fg_color="transparent")
        tabla_contenedor.pack(pady=10, fill=BOTH, expand=True)

        tree_frame = CTkFrame(tabla_contenedor, fg_color="#f0f0f0")
        tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 5), pady=5)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                    selectmode="extended", show="headings")
        self.my_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=self.my_tree.yview)


         #botones con las funciones
        frame_barra_derecha = CTkFrame(tabla_contenedor, fg_color="#000000", corner_radius=10)
        frame_barra_derecha.pack(side=RIGHT, fill=Y, padx=(5, 10), pady=5)

        self.img_label = CTkLabel(frame_barra_derecha, text="Imagen")
        self.img_label.pack(pady=30, padx=10)

        alquilar = CTkButton(frame_barra_derecha, text="Alquilar", fg_color="#00A86B", text_color="white",
                command=ADD)
        alquilar.pack(pady=5)

        limpiar = CTkButton(frame_barra_derecha, text="Limpiar", fg_color="#D32F2F",text_color="white",command=clear_entries_2)
        limpiar.pack(pady=5)


        tree_scroll.config(command=self.my_tree.yview)


        self.my_tree['columns']=("COD","Placa","Marca","Modelo")

        self.my_tree.column("COD",anchor=CENTER,width=140)
        self.my_tree.column("Placa",anchor=CENTER,width=140)
        self.my_tree.column("Marca",anchor=CENTER,width=140)
        self.my_tree.column("Modelo",anchor=CENTER,width=140)


        self.my_tree.heading("COD", text="COD Alquiler",anchor=CENTER)
        self.my_tree.heading("Placa", text="Placa",anchor=CENTER)
        self.my_tree.heading("Modelo", text="Vehículo Modelo",anchor=CENTER)
        self.my_tree.heading("Marca", text="Vehículo Marca",anchor=CENTER)
        

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#00A86B")

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
                background=[('selected',"#008fa8")])
        
        def validate_entry(text,new_text):
            if len(new_text) > 11:#Hace que no supere los 10 digitos
                return False
            return text.isdecimal()
        
        def validate_num_9(new_text):
            if len(new_text) > 9:
                return False
            return new_text == "" or new_text.isdigit()

        def validate_num_7(new_text):
            if len(new_text) > 7:
                return False
            return new_text == "" or new_text.isdigit()

        def validate_no_nums(new_text):
            return not any(char.isdigit() for char in new_text)

        def get_current_date():
            current_date = datetime.now().strftime('%d-%m-%Y')
            f1_entry.delete(0, END)
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
        
        def abrir_calendario(event, entry):
            top = Toplevel(self)
            top.title("Seleccionar fecha")
            top.geometry("290x250+650+300")
            top.transient(self) 
            top.focus_force()  
            #top.grab_set()

            cal = Calendar(top, date_pattern="dd-mm-yyyy", mindate=date.today())
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

        def mayusculas(event, entry):
            text = entry.get()
            if text:
                entry.delete(0, tk.END)
                entry.insert(0, text[0].upper() + text[1:])


        frame_inferior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"), corner_radius=10)
        frame_inferior.pack(padx=20, pady=10, fill="x")

        data_frame = CTkFrame(frame_inferior, fg_color="transparent")
        data_frame.pack(anchor="center")

        # CEDULA REDISEÑADA
        ci_label = CTkLabel(data_frame, text="Cedula", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        ci_label.grid(row=0, column=0, padx=10, pady=10)
        
        ci_frame = CTkFrame(data_frame, fg_color="transparent")
        ci_frame.grid(row=0, column=1, padx=10, pady=10)
        ci_prefix_menu = CTkOptionMenu(ci_frame, values=["V", "E", "J"], width=50, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), button_color="#00501B")
        ci_prefix_menu.pack(side=LEFT, padx=(0, 5))
        ci_num_entry = CTkEntry(ci_frame, width=90, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B",
                                validate="key", validatecommand=(data_frame.register(validate_num_9), "%P"))
        ci_num_entry.pack(side=LEFT)

        r_name_label = CTkLabel(data_frame, text="Nombre", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        r_name_label.grid(row=0, column=2, padx=10, pady=10)
        r_name_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B",
                                validate="key", validatecommand=(data_frame.register(validate_no_nums), "%P"))
        r_name_entry.grid(row=0, column=3, padx=10, pady=10)

        apell_label = CTkLabel(data_frame, text="Apellido", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        apell_label.grid(row=0, column=4, padx=10, pady=10)
        apell_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B",
                                validate="key", validatecommand=(data_frame.register(validate_no_nums), "%P"))
        apell_entry.grid(row=0, column=5, padx=10, pady=10)

        # RIF REDISEÑADO
        J_label = CTkLabel(data_frame, text="RIF", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        J_label.grid(row=0, column=6, padx=10, pady=10)
        
        rif_frame = CTkFrame(data_frame, fg_color="transparent")
        rif_frame.grid(row=0, column=7, padx=10, pady=10)
        rif_prefix_menu = CTkOptionMenu(rif_frame, values=["V", "E", "J", "G", "P", "C"], width=50, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), button_color="#00501B")
        rif_prefix_menu.set("V")
        rif_prefix_menu.pack(side=LEFT, padx=(0, 5))
        rif_num_entry = CTkEntry(rif_frame, width=90, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B",
                                 validate="key", validatecommand=(data_frame.register(validate_num_9), "%P"))
        rif_num_entry.pack(side=LEFT)

        e_name_label = CTkLabel(data_frame, text="Empresa", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        e_name_label.grid(row=1, column=0, padx=10, pady=10)
        e_name_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        e_name_entry.grid(row=1, column=1, padx=10, pady=10)

        dir_label = CTkLabel(data_frame, text="Direccion", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        dir_label.grid(row=1, column=2, padx=10, pady=10)
        dir_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        dir_entry.grid(row=1, column=3, padx=10, pady=10)

        # TELEFONO REDISEÑADO
        cell_label = CTkLabel(data_frame, text="Teléfono", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        cell_label.grid(row=1, column=4, padx=10, pady=10)
        
        tlf_frame = CTkFrame(data_frame, fg_color="transparent")
        tlf_frame.grid(row=1, column=5, padx=10, pady=10)
        tlf_prefix_menu = CTkOptionMenu(tlf_frame, values=["0414", "0424", "0416", "0426", "0412", "0422"], width=60, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), button_color="#00501B")
        tlf_prefix_menu.set("0414")
        tlf_prefix_menu.pack(side=LEFT, padx=(0, 5))
        tlf_num_entry = CTkEntry(tlf_frame, width=70, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B",
                                 validate="key", validatecommand=(data_frame.register(validate_num_7), "%P"))
        tlf_num_entry.pack(side=LEFT)

        f1_label = CTkLabel(data_frame, text="Fecha Inicial", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        f1_label.grid(row=1, column=6, padx=10, pady=10)
        f1_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        f1_entry.grid(row=1, column=7, padx=10, pady=10)

        f2_label = CTkLabel(data_frame, text="Fecha Final", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        f2_label.grid(row=2, column=0, padx=10, pady=10)
        f2_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        f2_entry.grid(row=2, column=1, padx=10, pady=10)

        plac_label = CTkLabel(data_frame, text="Placa", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        plac_label.grid(row=2, column=2, padx=10, pady=10)
        plac_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        plac_entry.grid(row=2, column=3, padx=10, pady=10)

        mar_label = CTkLabel(data_frame, text="Marca", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        mar_label.grid(row=2, column=4, padx=10, pady=10)
        mar_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        mar_entry.grid(row=2, column=5, padx=10, pady=10)

        modelo_label = CTkLabel(data_frame, text="Modelo", fg_color='transparent', text_color=("black", "white"), font=("Ubuntu", 16))
        modelo_label.grid(row=2, column=6, padx=10, pady=10)
        modelo_entry = CTkEntry(data_frame, fg_color=("#c2f1c1", "#2D2D2D"), text_color=("black", "white"), border_color="#00501B")
        modelo_entry.grid(row=2, column=7, padx=10, pady=10)

        r_name_entry.bind("<KeyRelease>", lambda e: mayusculas(e, r_name_entry))
        apell_entry.bind("<KeyRelease>", lambda e: mayusculas(e, apell_entry))
        e_name_entry.bind("<KeyRelease>", lambda e: mayusculas(e, e_name_entry))
        dir_entry.bind("<KeyRelease>", lambda e: mayusculas(e, dir_entry))
        f2_entry.bind("<Button-1>", lambda e: abrir_calendario(e, f2_entry))

        get_current_date()


        def select_record(e):
            f1_entry.delete(0,END)
            f2_entry.delete(0,END)
            # Limpiar nuevos campos
            ci_num_entry.delete(0, END)
            rif_num_entry.delete(0, END)
            tlf_num_entry.delete(0, END)
            
            r_name_entry.delete(0,END)
            apell_entry.delete(0,END)
            e_name_entry.delete(0,END)
            dir_entry.delete(0,END)
            plac_entry.delete(0,END)
            mar_entry.delete(0,END)
            modelo_entry.delete(0,END)

            selected = self.my_tree.focus()
            values = self.my_tree.item(selected,'values')
            if not values: return

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

        self.my_tree.bind("<ButtonRelease-1>", select_record)


        query_db()


    def actualizar_tree_2(self):
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
            SELECT a.COD_Alquiler, v.Placa, m.Nombre, o.Nombre
            FROM vehiculo v
            LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa
            RIGHT JOIN marca m ON m.ID = v.ID_Marca
            INNER JOIN modelo o ON v.ID_Modelo = o.ID
            WHERE a.COD_Alquiler IS NULL
            ORDER BY a.COD_Alquiler ASC;
        """)

        items = my_cursor.fetchall()
        for count, item in enumerate(items):
            tag = 'evenrow' if count % 2 == 0 else 'oddrow'
            self.my_tree.insert('', 'end', iid=count, values=item, tags=(tag,))

        mydb.close()
    



