import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
from tkinter import END, ttk, messagebox
from tkinter.font import BOLD
from forms.form_master import Principal
from forms.master_usuario_2 import usuario
import sqlite3
import bcrypt

class App:
    db_name='database_proyecto.db'
        
    
    def Validar_login_2(self, rif, password):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT Contraseña FROM Usuarios_2 WHERE Usuario = ?", (rif,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado is None:
                return False
            contraseña_almacenada = resultado[0]
            if bcrypt.checkpw(self.password_login.get().encode('utf-8'), contraseña_almacenada.encode('utf-8')):
                return True
            else:
                return False
    
    
    
    def Validar_login(self, rif, password):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT Contraseña FROM Usuarios WHERE Usuario = ?", (rif,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado is None:
                return False
            contraseña_almacenada = resultado[0]
            if bcrypt.checkpw(self.password_login.get().encode('utf-8'), contraseña_almacenada.encode('utf-8')):
                return True
            else:
                return False
        
    def Validar_formulario_completo(self):
        if self.usuario.get() and self.password_login.get():
            return True
        else:
            messagebox.showerror("ERROR DE INGRESO", "Ingrese su Usuario y contraseña!!!")
            return False
   
    

    def Login(self):
        try:
            if (self.Validar_formulario_completo()):
                rif= self.usuario.get()
                password= self.password_login.get()
                dato = self.Validar_login(rif, password)
                dato_2 = self.Validar_login_2(rif, password)
                if dato_2:
                    messagebox.showinfo("BIENVENIDO", "Datos ingresados correctamente")
                    self.ventana_login.destroy()
                    usuario()
                elif dato:
                    messagebox.showinfo("BIENVENIDO", "Datos ingresados correctamente")
                    self.ventana_login.destroy()
                    Principal()
        
                else:
                    messagebox.showerror("ERROR", "Usuario o contraseña incorrecto")
        except sqlite3.Error as e:
            messagebox.showerror("ERROR DE INGRESO", f"Error en la base de datos: {str(e)}")
                    
    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                        borderwidth=0,bg="black", cursor="hand2",activebackground="black", background="black")
        self.hide_button.place(x=860, y=420)
        self.password_login.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                        borderwidth=0,bg="black", cursor="hand2",activebackground="black" ,background="black")
        self.show_button.place(x=860, y=420)
        self.password_login.config(show='*')
            
    def recuperar_password(self):    
        class recuperar:
            db_name='database_proyecto.db'

            def __init__(self):
                self.window = Toplevel()
                self.window.title('Recuperar Contraseña')
                self.window.geometry('580x630+390+40')
                self.window.iconbitmap("imagenes\\letra-r.ico")
                self.window.resizable(0,0)
                self.window.config(bg="#145A32")


                self.frame_logo = Image.open('imagenes\\fondo.jpg')
                photo = ImageTk.PhotoImage(self.frame_logo)
                self.bg_recuperar = CTkLabel(self.window, image=photo)
                self.bg_recuperar.image = photo
                self.bg_recuperar.pack(fill='both', expand='yes')

                self.lgn_frame = CTkFrame(self.window, fg_color='#040405', border_color="#040405", corner_radius=10, border_width=20, width=450, height=560)
                self.lgn_frame.place(x=60, y=40)

                self.stilo = ttk.Style(self.lgn_frame)
                self.stilo.theme_use('clam')

                frame_form = Frame(self.window,bd=0,relief=SOLID,bg='#fcfcfc')
                frame_form.pack(side="right",expand=NO,fill=BOTH)

                #CUADRO SUPERIOR/TITULO DE INICIO
                self.title = "Recuperar Contraseña"
                self.heading = Label(self.lgn_frame, text=self.title, font=('yu gothic ui', 20, "bold"), bg="#040405",
                                    fg='white',
                                    bd=5,
                                    relief=FLAT)
                self.heading.place(x=50, y=8, width=350, height=30)


                self.sign_imagen = Image.open('imagenes\\codigo.png')
                photo = ImageTk.PhotoImage(self.sign_imagen)
                self.sign_imagen_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.sign_imagen_label.image = photo
                self.sign_imagen_label.place(x=190, y=50)

                #CUADRO CENTARL/DONDE SE ENCUENTRAN LOS ENTRYS Y BOTONES
                frame_form_fill = CTkFrame(frame_form,height=50,fg_color='#008d62', corner_radius=0)
                frame_form_fill.pack(side="bottom",expand=YES,fill=BOTH)

                #USUARIO
                self.etiqueta_rif = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.etiqueta_rif.place(x=30, y=100)
                self.rif = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
                self.rif.place(x=60, y=136, width=310)

                self.usuario_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.usuario_linea.place(x=30, y=159)

                self.username_icon = Image.open('imagenes\\username_icon.png')
                photo = ImageTk.PhotoImage(self.username_icon)
                self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.username_icon_label.image = photo
                self.username_icon_label.place(x=30, y=132)

                #Preguntas de seguridad
                self.label_pregunta = Label(self.lgn_frame, text="Seleccione la pregunata de seguridad", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.label_pregunta.place(x=30, y=170)
                self.lista_pregunta=ctk.CTkComboBox(self.lgn_frame,font=('yu gothic ui',15),values=["Nombre de su primera mascota?","Comida favorita?","Bebida favorita?", "En que ciudad naciste ?"],state="readonly")
                self.lista_pregunta.place(x=70, y=205)
                self.lista_pregunta.configure(width=300)

                self.icon_combobox = Image.open('imagenes\\pregunta.png')
                photo = ImageTk.PhotoImage(self.icon_combobox)
                self.icon_combobox_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.icon_combobox_label.image = photo
                self.icon_combobox_label.place(x=28, y=201)

                #Respuesta
                self.etiqueta_respuesta = Label(self.lgn_frame, text="Respueta", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.etiqueta_respuesta.place(x=30, y=240)
                self.respuesta = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
                self.respuesta.place(x=65, y=280, width=310)

                self.respuesta_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.respuesta_linea.place(x=30, y=305)

                self.icon_respuesta = Image.open('imagenes\\respuesta.png')
                photo = ImageTk.PhotoImage(self.icon_respuesta)
                self.icon_respuesta_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.icon_respuesta_label.image = photo
                self.icon_respuesta_label.place(x=28, y=269)


                #CONTRASEÑA
                self.etiqueta_contraseña = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.etiqueta_contraseña.place(x=30, y=315)
                self.password = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
                self.password.place(x=60, y=351, width=310)


                self.password_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.password_linea.place(x=30, y=375)

                self.password_icon = Image.open('imagenes\\password_icon.png')
                photo = ImageTk.PhotoImage(self.password_icon)
                self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.password_icon_label.image = photo
                self.password_icon_label.place(x=30, y=346)

                
                #CONFIRMAR CONTRASEÑA
                self.repetir_password = Label(self.lgn_frame, text="Repetir Password", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.repetir_password.place(x=30, y=385)
                self.repetir = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
                self.repetir.place(x=60, y=422, width=310)

                self.password_linea_2 = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.password_linea_2.place(x=30, y=446)

                self.password_repetir = Image.open('imagenes\\password_icon.png')
                photo = ImageTk.PhotoImage(self.password_repetir)
                self.password_icon_repetir = Label(self.lgn_frame, image=photo, bg='#040405')
                self.password_icon_repetir.image = photo
                self.password_icon_repetir.place(x=30, y=419)

                self.show_image = ImageTk.PhotoImage \
                    (file='imagenes\\ojo-abierto.png')

                self.hide_image = ImageTk.PhotoImage \
                    (file='imagenes\\ojo.png')
                
                self.salir_image = ImageTk.PhotoImage \
                    (file='imagenes\\salir.png')

                #MOSTRAR CONTRASEÑAS
                self.mostrar_password = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                        borderwidth=0, cursor="hand2",bg="black",activebackground="black", background="black")
                self.mostrar_password.place(x=390, y=420)

                self.mostrar_password_repetir = Button(self.lgn_frame, image=self.show_image, relief=FLAT,
                                        borderwidth=0, cursor="hand2",bg="black",activebackground="black", background="black")
                self.mostrar_password_repetir.place(x=390, y=345)


                #SALIR
                self.salir = Button(self.lgn_frame, image=self.salir_image, command=self.regresar, relief=FLAT,
                                        borderwidth=0, cursor="hand2",bg="black",activebackground="black", background="black")
                self.salir.place(x=20, y=510)

                

                #BOTÓN
                self.inicio = CTkButton(self.lgn_frame, text='Recuperar', command=self.Restablecer_contraseña, font=("yu gothic ui", 20, "bold"), width=150, height=40,
                                    hover_color='#a9dfbf', cursor='hand2', fg_color='#145a32', corner_radius=20)
                self.inicio.place(x=140, y=470)
                self.inicio.bind("<Return>")

            def show(self):
                self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                                borderwidth=0,bg="black", cursor="hand2",activebackground="black", background="black")
                self.hide_button.place(x=860, y=420)
                self.password.config(show='')

            def hide(self):
                self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                                borderwidth=0,bg="black", cursor="hand2",activebackground="black" ,background="black")
                self.show_button.place(x=860, y=420)
                self.password.config(show='*')
                self.window.mainloop

            def regresar(self):
                self.window.destroy()

        
            
            def Ejecutar_consulta(self, query, parameters=()):
                with sqlite3.connect(self.db_name) as conexion:
                    cursor=conexion.cursor()
                    result=cursor.execute(query,parameters)
                    conexion.commit()
                return result
            
            def Limpiar_formulario_recuperar(self):
                self.rif.delete(0, END)
                self.respuesta.delete(0, END)
                self.password.delete(0, END)
                self.repetir.delete(0, END)
                
            def Validar_formulario_completo_recuperar(self):
                    if len(self.rif.get()) !=0 and len(self.password.get()) !=0 and len(self.repetir.get()) !=0 and len(self.respuesta.get()) !=0:
                        return True
                    else:
                        messagebox.showerror("ERROR", "Complete todos los campos del formulario")
                    
            def Validar_contraseña_recuperar(self):
                if(str(self.password.get()) == str(self.repetir.get())):
                    return True
                else:
                    messagebox.showerror("ERROR DE RECUPERACION", "Contraseñas no coinciden")
        
            def Buscar_usuario(self, rif, respuesta):
                with sqlite3.connect(self.db_name) as conexion:
                    cursor=conexion.cursor()
                    sql=f"SELECT * FROM Usuarios WHERE Usuario = '{rif}' AND Respuesta = '{respuesta}'"
                    cursor.execute(sql)
                    busqueda= cursor.fetchall() # obtener respuesta como lista
                    cursor.close()
                    return busqueda

            def Validar_datos_usuario(self):
                try:
                    rif= self.rif.get()
                    respuesta=self.respuesta.get()
                    busqueda = self.Buscar_usuario(rif, respuesta)
                    if (busqueda != []):
                        return True
                    else:
                        messagebox.showerror("ERROR DE RECUPERACION", "Datos de recuperacion no son correctos")
                except:
                    messagebox.showerror("ERROR DE RECUPERACION", "Datos de recuperacion no son correctos")

            def Restablecer_contraseña(self):
                hashed_password = bcrypt.hashpw(self.password.get().encode('utf-8'), bcrypt.gensalt())
                if self.Validar_formulario_completo_recuperar() and self.Validar_datos_usuario() and self.Validar_contraseña_recuperar():
                    query='UPDATE Usuarios SET Contraseña = (?) WHERE Usuario= (?)'
                    parameters = (hashed_password.decode('utf-8'), self.rif.get())
                    self.Ejecutar_consulta(query, parameters)
                    messagebox.showinfo("CONTRASEÑA RECUPERADA", f'Contraseña actualizada correctamente')
                    print('DATOS ACTUALIZADO')
                    self.Limpiar_formulario_recuperar()
                    self.window.destroy

        recuperar()
        

    def recuperar_preguntas(self):    
        class preguntas:
            db_name='database_proyecto.db'

            def __init__(self):
                self.window = Toplevel()
                self.window.title('Recuperar Preguntas')
                self.window.geometry('580x630+390+40')
                self.window.iconbitmap("imagenes\\letra-r.ico")
                self.window.resizable(0,0)

                self.frame_logo = Image.open('imagenes\\fondo.jpg')
                photo = ImageTk.PhotoImage(self.frame_logo)
                self.bg_recuperar = CTkLabel(self.window, image=photo)
                self.bg_recuperar.image = photo
                self.bg_recuperar.pack(fill='both', expand='yes')

                self.lgn_frame = CTkFrame(self.window, fg_color='#040405', border_color="#040405", corner_radius=10, border_width=20, width=450, height=560)
                self.lgn_frame.place(x=60, y=40)



                frame_form = Frame(self.window,bd=0,relief=SOLID,bg='#fcfcfc')
                frame_form.pack(side="right",expand=NO,fill=BOTH)

                #CUADRO SUPERIOR/TITULO DE INICIO
                self.title = "Recuperar Preguntas"
                self.heading = Label(self.lgn_frame, text=self.title, font=('yu gothic ui', 20, "bold"), bg="#040405",
                                    fg='white',
                                    bd=5,
                                    relief=FLAT)
                self.heading.place(x=50, y=7, width=350, height=35)


                self.sign_imagen = Image.open('imagenes\\preguntas_logo.png')
                photo = ImageTk.PhotoImage(self.sign_imagen)
                self.sign_imagen_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.sign_imagen_label.image = photo
                self.sign_imagen_label.place(x=190, y=43)

                #CUADRO CENTARL/DONDE SE ENCUENTRAN LOS ENTRYS Y BOTONES
                frame_form_fill = CTkFrame(frame_form,height=50,fg_color='#008d62', corner_radius=0)
                frame_form_fill.pack(side="bottom",expand=YES,fill=BOTH)

                #CODIGO DE SEGURIDAD
                self.codigo_seguridad = Label(self.lgn_frame, text="Codigo de seguridad", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.codigo_seguridad.place(x=30, y=100)
                self.cod = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui ", 12, "bold"), show="*", insertbackground = '#6b6a69')
                self.cod.place(x=60, y=136, width=310)

                self.coigo_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.coigo_linea.place(x=30, y=159)

                self.username_icon = Image.open('imagenes\\password_icon.png')
                photo = ImageTk.PhotoImage(self.username_icon)
                self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.username_icon_label.image = photo
                self.username_icon_label.place(x=30, y=132)

                #Preguntas de seguridad
                self.primera_pregunta = Label(self.lgn_frame, text="Nombre de su primera mascota?", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.primera_pregunta.place(x=30, y=170)
                self.primera = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
                self.primera.place(x=65, y=210, width=310)

                self.primera_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.primera_linea.place(x=30, y=234)

                self.icon_combobox = Image.open('imagenes\\1.png')
                photo = ImageTk.PhotoImage(self.icon_combobox)
                self.icon_primera_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.icon_primera_label.image = photo
                self.icon_primera_label.place(x=30, y=198)

                #SEGUNDA
                self.segunda_pregunta = Label(self.lgn_frame, text="Comida Favorita?", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.segunda_pregunta.place(x=30, y=240)
                self.segunda = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
                self.segunda.place(x=65, y=280, width=310)

                self.segunda_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.segunda_linea.place(x=30, y=304)

                self.icon_respuesta = Image.open('imagenes\\2.png')
                photo = ImageTk.PhotoImage(self.icon_respuesta)
                self.icon_segunda_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.icon_segunda_label.image = photo
                self.icon_segunda_label.place(x=30, y=268)


                #CONTRASEÑA
                self.tercera_pregunta = Label(self.lgn_frame, text="Bebida Favorita?", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.tercera_pregunta.place(x=30, y=315)
                self.tercera = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui", 12, "bold"), insertbackground = '#6b6a69')
                self.tercera.place(x=65, y=351, width=310)


                self.tercera_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.tercera_linea.place(x=30, y=375)

                self.password_icon = Image.open('imagenes\\3.png')
                photo = ImageTk.PhotoImage(self.password_icon)
                self.tercer_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
                self.tercer_icon_label.image = photo
                self.tercer_icon_label.place(x=30, y=339)
                
                self.salir_image = ImageTk.PhotoImage \
                    (file='imagenes\\salir.png')

                #SALIR
                self.salir = Button(self.lgn_frame, image=self.salir_image, command=self.regresar, relief=FLAT,
                                        borderwidth=0, cursor="hand2",bg="black",activebackground="black", background="black")
                self.salir.place(x=20, y=510)

                
                #Cuarta
                self.cuarta_pregunta = Label(self.lgn_frame, text="En que ciudad naciste?", bg="#040405", fg="#4f4e4d",
                                            font=("yu gothic ui", 13, "bold"))
                self.cuarta_pregunta.place(x=30, y=385)
                self.cuarta = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                            font=("yu gothic ui", 12, "bold"), insertbackground = '#6b6a69')
                self.cuarta.place(x=65, y=422, width=310)

                self.cuarta_linea = Canvas(self.lgn_frame, width=350, height=2.0, bg="#bdb9b1", highlightthickness=0)
                self.cuarta_linea.place(x=30, y=446)

                self.password_repetir = Image.open('imagenes\\4.png')
                photo = ImageTk.PhotoImage(self.password_repetir)
                self.cuarto_icon = Label(self.lgn_frame, image=photo, bg='#040405')
                self.cuarto_icon.image = photo
                self.cuarto_icon.place(x=30, y=410)

                

                #BOTÓN
                self.inicio = CTkButton(self.lgn_frame, text='Recuperar', command=self.actualizar_datos, font=("yu gothic ui", 20, "bold"), width=150, height=40,
                                    hover_color='#a9dfbf', cursor='hand2', fg_color='#145a32', corner_radius=20)
                self.inicio.place(x=140, y=470)
                self.inicio.bind("<Return>")                

            def regresar(self):
                self.window.destroy()
                App()

            
            
            
            def Limpiar_formulario_recuperar(self):
                self.cod.delete(0, END)
                self.primera.delete(0, END)
                self.segunda.delete(0, END)
                self.tercera.delete(0, END)
                self.cuarta.delete(0, END)
                
            def Validar_formulario_completo_recuperar(self):
                    if len(self.cod.get()) !=0 and len(self.primera.get()) !=0 and len(self.segunda.get()) !=0 and len(self.tercera.get()) !=0 and len(self.cuarta.get()) !=0:
                        return True
                    else:
                        messagebox.showerror("ERROR", "Complete todos los campos del formulario")
                    
        
            def Buscar_respuesta(self, cod):
                with sqlite3.connect(self.db_name) as conexion:
                    cursor=conexion.cursor()
                    sql=f"SELECT * FROM Usuarios WHERE Seguridad = '{cod}'"
                    cursor.execute(sql)
                    busqueda= cursor.fetchall()
                    cursor.close()
                    return busqueda

            def Validar_datos_respuesta(self):
                try:
                    cod= self.cod.get()
                    busqueda = self.Buscar_respuesta(cod)
                    if (busqueda != []):
                        return True
                    else:
                        messagebox.showerror("ERROR DE RECUPERACION", "Datos de recuperacion no son correctos")
                except:
                    messagebox.showerror("ERROR DE RECUPERACION", "Datos de recuperacion no son correctos")

            def actualizar_datos(self):
                if  self.Validar_formulario_completo_recuperar() and self.Validar_datos_respuesta():
                    messagebox.showinfo("PREGUNTA RECUPERADA", f'Pregunta actualizada correctamente')
                    conn = sqlite3.connect('database_proyecto.db')
                    cursor = conn.cursor()

                    nuevos_datos = [self.primera.get(), self.segunda.get(), self.tercera.get(), self.cuarta.get()]
                    for i in range(1, 5):
                        cursor.execute('UPDATE Usuarios SET Respuesta = ? WHERE id = ?', (nuevos_datos[i-1], i))
                        
                    self.Limpiar_formulario_recuperar()

                    conn.commit()
                    conn.close()


                # Conexión a la base de datos
                conn = sqlite3.connect('database_proyecto.db')
                cursor = conn.cursor()

                # Crear tabla si no existe
                cursor.execute('CREATE TABLE IF NOT EXISTS datos(id INTEGER PRIMARY KEY, dato TEXT)')

                # Insertar datos de ejemplo si la tabla está vacía
                cursor.execute('SELECT COUNT(*) FROM Usuarios')
                if cursor.fetchone()[0] == 0:
                    cursor.execute('INSERT INTO Usuarios (dato) VALUES (?)', ('Dato 1',))
                    cursor.execute('INSERT INTO Usuarios (dato) VALUES (?)', ('Dato 2',))
                    cursor.execute('INSERT INTO Usuarios (dato) VALUES (?)', ('Dato 3',))
                    cursor.execute('INSERT INTO Usuarios (dato) VALUES (?)', ('Dato 4',))

                        
                conn.commit()
                conn.close()
            

        preguntas()

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                borderwidth=0,bg="black", cursor="hand2",activebackground="black", background="black")
        self.hide_button.place(x=860, y=420)
        self.password_login.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                borderwidth=0,bg="black", cursor="hand2",activebackground="black" ,background="black")
        self.show_button.place(x=860, y=420)
        self.password_login.config(show='*')
        
    def __init__(self):
        self.ventana_login = CTk()
        self.ventana_login.title('Inicio de sesion')
        self.ventana_login.geometry('1280x680+35+15')
        self.ventana_login.iconbitmap("imagenes\\letra-r.ico")
        self.ventana_login.resizable()
        self.ventana_login._set_appearance_mode("dark")


        self.frame_logo = Image.open('imagenes\\fondo.jpg')
        photo = ImageTk.PhotoImage(self.frame_logo)
        self.bg_panel = CTkLabel(self.ventana_login, image=photo, fg_color="#040405", bg_color="#040405")
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')


        self.lgn_frame = CTkFrame(self.ventana_login, fg_color='#040405', border_color="#040405", corner_radius=10, border_width=20, width=950, height=600)
        self.lgn_frame.place(x=200, y=70)



        frame_form = Frame(self.ventana_login,bd=0,relief=SOLID,bg='#fcfcfc')
        frame_form.pack(side="right",expand=YES,fill=BOTH)

        #CUADRO SUPERIOR/TITULO DE INICIO
        self.title = "Iniciar Sesión"
        self.heading = Label(self.lgn_frame, text=self.title, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)


        self.side_image = Image.open('imagenes\\Reych.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        #CUADRO SUPERIOR/TITULO DE INICIO
        self.sing_ing = CTkLabel(self.lgn_frame, text="Sing in", font=('yu gothic ui', 23, "bold"))
        self.sing_ing.place(x=650, y=242)

        self.sign_imagen = Image.open('imagenes\\usuario.png')
        photo = ImageTk.PhotoImage(self.sign_imagen)
        self.sign_imagen_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_imagen_label.image = photo
        self.sign_imagen_label.place(x=620, y=110)

        #CUADRO CENTARL/DONDE SE ENCUENTRAN LOS ENTRYS Y BOTONES
        frame_form_fill = CTkFrame(frame_form,height=50,fg_color='#008d62', corner_radius=0)
        frame_form_fill.pack(side="bottom",expand=YES,fill=BOTH)


        #USUARIO
        self.etiqueta_usuario = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.etiqueta_usuario.place(x=550, y=300)

        etiqueta_usuario = CTkLabel(frame_form_fill,text="hola",font=('BOLD',14),text_color="white",fg_color='transparent',anchor="w")
        etiqueta_usuario.pack(fill=X,padx=20,pady=5)
        self.usuario = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.usuario.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)

        self.username_icon = Image.open('imagenes\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        #CONTRASEÑA
        self.etiqueta_password = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.etiqueta_password.place(x=550, y=380)

        self.password_login = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_login.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        self.password_icon = Image.open('imagenes\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=412)

        self.show_image = ImageTk.PhotoImage \
            (file='imagenes\\ojo-abierto.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='imagenes\\ojo.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                borderwidth=0, cursor="hand2",bg="black",activebackground="black", background="black")
        self.show_button.place(x=860, y=420)



        #CAMBIAR CONTRASEÑA
        self.boton_recuperar_password = Button(self.lgn_frame, text="Olvido su Contraseña ?",
                                    font=("yu gothic ui", 13), command=self.recuperar_password, fg="white", relief=FLAT,
                                    activebackground="#040405"
                                    , borderwidth=0, background="#040405", cursor="hand2")
        self.boton_recuperar_password.place(x=620, y=510)

        #CAMBIAR PREGUNTAS
        self.boton_recuperar_preguntas = Button(self.lgn_frame, command=self.recuperar_preguntas,text="Olvido sus Preguntas ?",
                                            font=("yu gothic ui", 13), fg="white", relief=FLAT,
                                            activebackground="#040405"
                                            , borderwidth=0, background="#040405", cursor="hand2")
        self.boton_recuperar_preguntas.place(x=620, y=540)

        
        #BOTÓN
        self.inicio = CTkButton(self.lgn_frame, text='Iniciar', font=("yu gothic ui", 20, "bold"), width=150, height=40,
                            hover_color='#a9dfbf', command=self.Login, cursor='hand2', fg_color='#145a32', corner_radius=20)
        self.inicio.place(x=630, y=460)
        self.inicio.bind("<Return>")

        
        def limitar_entry():
            if len(self.password_login.get()) >= 8:
                self.password_login.delete(8, 'end')
        self.password_login.bind('<KeyRelease>', limitar_entry)


        self.ventana_login.mainloop()