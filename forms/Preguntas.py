import customtkinter as ctk
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import END, ttk, messagebox


class preguntas:
            db_name='database_proyecto.db'

            def __init__(self):
                self.window = CTk()
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
                self.inicio = CTkButton(self.lgn_frame, text='Recuperar', font=("yu gothic ui", 20, "bold"), width=150, height=40,
                                    hover_color='#a9dfbf', cursor='hand2', fg_color='#145a32', corner_radius=20)
                self.inicio.place(x=140, y=470)
                self.inicio.bind("<Return>")                

            def regresar(self):
                self.window.destroy()
preguntas()