from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import mysql.connector
from customtkinter import *
from forms.frame_datos import FrameDatosDetallados
from forms.imprimir_funcion import imprimir_todos
from PIL import Image

def ventana_imprimir():

    class imprimir:
        def __init__(self):
            self.root = tk.Toplevel()
            self.root.title('ALQUITECH')
            self.root.geometry("900x410+250+150")
            self.root.config(background='#EEEEEE')


            self.barra_visible = True
            self.barra_width = 200  

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                port="3306",
                database="control_alquiler_Reych"
            )
            self.my_cursor = mydb.cursor()


            frame_form = Frame(self.root, bd=0, relief=SOLID, bg="#0E0F0F", height=50)
            frame_form.pack(side="top", expand=NO, fill=BOTH)

            frame_form_top = Frame(frame_form, bd=0, relief=SOLID, bg='black')
            frame_form_top.pack(side="top", fill=X)

            self.frame_main = CTkFrame(self.root, fg_color='white')
            self.frame_main.pack(side="left", expand=True, fill=BOTH)

            self.frame_form_l = CTkFrame(self.frame_main, fg_color="#0E0F0F", width=self.barra_width)
            self.frame_form_l.pack(side="left", fill=Y)
            self.frame_form_l.pack_propagate(False)

            frame_top = CTkFrame(self.frame_form_l, fg_color="transparent")
            frame_top.pack(side="top", fill=X)

            title = CTkLabel(master=frame_top, text="Alquitech",
                            font=('YRSA SEMIBOLD', 40),
                            text_color="white", pady=1)
            title.pack(expand=YES, fill=BOTH, pady=5, padx=15)

            imglogo = Image.open("imagenes/Reych.png")
            bg = CTkLabel(master=frame_top, text=None,
                            image=CTkImage(dark_image=imglogo, light_image=imglogo, size=(170, 170)))
            bg.pack(anchor="center", padx=30, pady=1)

            frame_botones = CTkFrame(self.frame_form_l, fg_color="transparent")
            frame_botones.pack(side="top", fill=X, pady=20)

            img = Image.open("imagenes/imprimir_fila.png")
            imprimir_seleccion = CTkImage(dark_image=img, light_image=img, size=(30,30))
            imprimir_fila = CTkButton(frame_botones, text="Imprimir Seleccion",
                                    fg_color="transparent",command=self.imprimir_datos,compound="left",image=imprimir_seleccion,hover_color="#00501B", text_color="white",
                                    width=150, height=30,
                                    font=("Ubuntu", 18))
            imprimir_fila.pack(fill=X, pady=5, padx=2)

            img = Image.open("imagenes/registro.png")
            imprimir_icon_todo = CTkImage(dark_image=img, light_image=img, size=(30,30))
            imprimir_todo = CTkButton(frame_botones, text="Imprimir todo",
                                    fg_color="transparent", command=imprimir_todos,compound="left",image=imprimir_icon_todo,hover_color="#00501B",text_color="white",
                                    width=150, height=30,
                                    font=("Ubuntu", 18))
            imprimir_todo.pack(fill=X,pady=5, padx=2)

            frame_botones2 = CTkFrame(self.frame_form_l, fg_color="transparent")
            frame_botones2.pack(side="bottom", fill=X, pady=20)

            self.ocultar_btn = CTkButton(frame_form, text="☰ Ocultar",
                                        text_color="white", hover_color="#00501B",fg_color="#0E0F0F",
                                        command=self.toggle_barra)
            self.ocultar_btn.pack(anchor="nw", padx=10, pady=10)

            self.frame_contenido_principal = CTkFrame(self.frame_main, fg_color='white')
            self.frame_contenido_principal.pack(expand=True, fill=BOTH, padx=10, pady=10)

            self.tree_frame = CTkFrame(self.frame_contenido_principal, corner_radius=20)
            self.tree_frame.pack(pady=20, expand=True, fill=BOTH)

            tree_scroll = Scrollbar(self.tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=tree_scroll.set,
                                        selectmode="extended", show="headings")
            self.my_tree.pack(expand=True, fill=BOTH)
            tree_scroll.config(command=self.my_tree.yview)

            self.my_tree['columns']=("COD","RIF","Empresa","TLF","Direccion","Cedula","Nombre","Apellido","Placa","Color","Año","Marca","Modelo")
            for col in self.my_tree['columns']:
                self.my_tree.column(col, anchor=CENTER, width=100)
                self.my_tree.heading(col, text=col, anchor=CENTER)

            self.my_tree.tag_configure('oddrow', background="white")
            self.my_tree.tag_configure('evenrow', background="#00A86B")

            self.query_db()

            self.frame_datos_detallados = CTkFrame(self.frame_main, fg_color='white')
            label_hola = CTkLabel(self.frame_datos_detallados, text="¡Esta es la pantalla de Datos Detallados.", text_color="black",
                                font=("Ubuntu", 20))
            label_hola.pack(pady=50)

            self.frame_vehiculos_disponibles = CTkFrame(self.frame_main, fg_color='white')
            label_hola = CTkLabel(self.frame_vehiculos_disponibles, text="¡Esta es la pantalla de vehiculos disponibles.", text_color="black",
                                font=("Ubuntu", 20))
            label_hola.pack(pady=50)


            self.root.mainloop()

        def imprimir_datos(self):
            if hasattr(self, "frame_datos_detallados"):
                FrameDatosDetallados.imprimir_fila_seleccionada(self, parent=self.root)
            else:
                messagebox.showwarning("Atención", "No hay datos detallados cargados.", parent=self.root)


        def toggle_barra(self):
            if self.barra_visible:
                self.frame_form_l.configure(width=0)
                self.ocultar_btn.configure(text="☰ Mostrar")
            else:
                self.frame_form_l.configure(width=self.barra_width)
                self.ocultar_btn.configure(text="☰ Ocultar")
            self.barra_visible = not self.barra_visible

        def query_db(self):
            self.my_cursor.execute("SELECT a.COD_Alquiler, c.RIF, c.nombre, c.telefono, c.direccion, r.CI, r.nombre, r.apellido, v.Placa, v.Color,v.Año, m.Nombre, o.Nombre FROM contratista c INNER JOIN alquiler a ON c.RIF = a.RIF_Empresa INNER JOIN representante r ON c.Representante_CI = r.CI INNER JOIN vehiculo v ON a.Placa_Vehiculo = v.Placa INNER JOIN marca m ON v.ID_Marca = m.ID INNER JOIN modelo o ON o.ID_Marca = m.ID ORDER BY a.COD_Alquiler ASC;")
            records = self.my_cursor.fetchall()
            for i, record in enumerate(records):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.my_tree.insert('', 'end', iid=i, values=record, tags=(tag,))
                
    imprimir()

