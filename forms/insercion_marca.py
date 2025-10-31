from tkinter import *
from tkinter import ttk
import mysql.connector
from customtkinter import *
from tkinter import messagebox


def vehiculo_marca():
    class vehiculo:
        def __init__(self):
            self.root = Tk()
            self.root.title('DISPLAY')
            self.root.geometry("170x320")
            self.root.resizable(False,False)
            self.root.config(background='#e3f2fd')#c2f1c1                                  #NARANJA

            mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                port = "3306",
                database = "control_alquiler_Reych"
            )

            my_cursor = mydb.cursor()

            frame_form = CTkFrame(self.root,fg_color='#005954',height=5, corner_radius=00)
            frame_form.pack(side="top",expand=NO,fill=Y)

            titulo = CTkLabel(frame_form, text="Ingrese Sus datos",fg_color="transparent")
            titulo.pack(side="top",fill=X, pady=20)

            frame_entry = CTkFrame(frame_form, fg_color="transparent")
            frame_entry.pack(side="top",fill=X, pady=20)

            def agregar():
                mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "123456",
                            port = "3306",
                            database = "control_alquiler_Reych"
                        )

                my_cursor = mydb.cursor()

                sql = '''INSERT INTO marca (ID,Nombre) VALUES(%s,%s)'''
                values = (codigo_marca.get(),nombre_marca.get())
                sql2 = '''INSERT INTO modelo (Nombre, ID_Marca) VALUES(%s,%s)'''
                values2 = (nombre_modelo.get(),codigo_marca.get())
                try:
                            my_cursor.execute(sql,values)
                            mydb.commit()
                            my_cursor.execute(sql2,values2)
                            mydb.commit()
                            titulo = 'Ingresión'
                            mensaje = 'Vehiculo agregado con exito'
                            messagebox.showinfo(titulo, mensaje)
                except:
                            titulo = 'Alquilado'
                            mensaje = 'Ocurrio un problema'
                            messagebox.showinfo(titulo, mensaje)

            cod_marca = CTkLabel(frame_entry, text="Codigo")
            cod_marca.grid(row=0,column=0)
            codigo_marca = CTkEntry(frame_entry,  fg_color="#003d3c", border_color="#00bfae")
            codigo_marca.grid(padx=15,row=1, column=0)

            name_marca = CTkLabel(frame_entry, text="Marca")
            name_marca.grid(row=2,column=0)
            nombre_marca = CTkEntry(frame_entry,  fg_color="#003d3c", border_color="#00bfae")
            nombre_marca.grid(row=3,column=0)

            name_modelo = CTkLabel(frame_entry, text="Modelo")
            name_modelo.grid(row=4,column=0)
            nombre_modelo = CTkEntry(frame_entry,  fg_color="#003d3c", border_color="#00bfae")
            nombre_modelo.grid(row=5,column=0)

            agreg = CTkButton(frame_entry, text="Agregar", command=agregar, fg_color="#005954")
            agreg.grid(pady=20,row=6,column=0)

            self.root.mainloop()
    vehiculo()