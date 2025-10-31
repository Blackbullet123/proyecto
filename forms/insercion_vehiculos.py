from tkinter import *
from tkinter import ttk
import mysql.connector
from customtkinter import *
from tkinter import messagebox
from insercion_marca import vehiculo_marca

def insertar():
    class Datos:
        def __init__(self):
            self.root = Tk()
            self.root.title('INSERTAR')
            self.root.geometry("600x420")
            self.root.config(background='#e3f2fd')#c2f1c1                                  #NARANJA

            barra_menu = Menu()
            menu_archivo = Menu(barra_menu,tearoff=False)
            menu_archivo.add_command(label='Nuevo',accelerator='Ctrl+N')
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

                my_cursor.execute("SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca")
                records = my_cursor.fetchall()

                count = 0

                for record in records:
                    if count % 2 == 0:
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('evenrow',))
                    else: 
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('oddrow',))

                    count += 1

                conn.commit()
                conn.close()
                conn.close()


            style = ttk.Style()

            style.theme_use('clam')

            style.configure(
                "Treeview",
                background="lightgreen",
                foreground="black",
                rowheight=25,
                fieldbackground="#FCFCFC"
            )

            style.map('Treeview',
                    background=[('selected',"#003d3c")])

            frame_form = Frame(self.root,bd=0,relief=SOLID,bg='#fcfcfc',height=50)
            frame_form.pack(side="top",expand=NO,fill=BOTH)

            frame_form_top = Frame(frame_form, bd=0, relief=SOLID,bg='black')
            frame_form_top.pack(side="top",fill=X)
            title = Label(frame_form_top,text="Vehiculos",font=('BOLD',25),fg="#fcfcfc",bg='#005954',pady=5)#008259
            title.pack(expand=YES,fill=BOTH)

            frame_form_left = CTkFrame(self.root,fg_color='transparent',height=50)
            frame_form_left.pack(side="left",expand=NO,fill=BOTH)#, pady=20

            frame_form_l = CTkFrame(frame_form_left,fg_color='#005954', width=200, corner_radius=0)
            frame_form_l.pack(side="left",fill=Y)

            titulo = CTkLabel(frame_form_l, text="Ingrese Sus datos",fg_color="transparent",
                              font=("Ubuntu",18),text_color="white")
            titulo.pack(side="top",fill=X, pady=20)

            frame_entry = CTkFrame(frame_form_l, fg_color="transparent")
            frame_entry.pack(side="top",fill=X, pady=20)


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

                my_cursor.execute("SELECT m.ID, v.Placa, m.Nombre, o.Nombre, v.Color, v.Año FROM vehiculo v LEFT JOIN alquiler a ON a.Placa_Vehiculo = v.Placa RIGHT JOIN marca m ON m.ID = v.ID_Marca INNER JOIN modelo o ON m.ID = o.ID_Marca")
                records = my_cursor.fetchall()

                count = 0

                for record in records:
                    if count % 2 == 0:
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('evenrow',))
                    else: 
                        my_tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3], record[4],record[5]),tags=('oddrow',))

                    count += 1

                conn.commit()
                conn.close()

            def agregar():
                mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "123456",
                            port = "3306",
                            database = "control_alquiler_Reych"
                        )

                my_cursor = mydb.cursor()

                #sql = '''INSERT INTO marca (ID,Nombre) VALUES(%s,%s)'''
                #values = (codigo_marca.get(),nombre_marca.get())
                #sql2 = '''INSERT INTO modelo (Nombre, ID_Marca) VALUES(%s,%s)'''
                #values2 = (nombre_modelo.get(),codigo_marca.get())
                sql3 = '''INSERT INTO vehiculo (Placa, Color, Año, ID_Marca) VALUES (%s,%s,%s,%s)'''
                values3 = (placa_entry.get(), color_entry.get(),año_entry.get(), codigo_marca.get())
                try:
                            #my_cursor.execute(sql,values)
                            #mydb.commit()
                            #my_cursor.execute(sql2,values2)
                            #mydb.commit()
                            my_cursor.execute(sql3,values3)
                            mydb.commit()
                            titulo = 'Ingresión'
                            mensaje = 'Vehiculo agregado con exito'
                            messagebox.showinfo(titulo, mensaje)
                except:
                            titulo = 'Alquilado'
                            mensaje = 'Ocurrio un problema'
                            messagebox.showinfo(titulo, mensaje)
                finally:
                     actualizar_tree()

            def eliminar():
                mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "123456",
                            port = "3306",
                            database = "control_alquiler_Reych"
                        )

                my_cursor = mydb.cursor()

                #sql = "DELETE FROM marca WHERE ID = '{0}'"
                #sql2 = "DELETE FROM modelo WHERE ID_Marca = '{0}'"
                sql3 = "DELETE FROM vehiculo WHERE Placa = '{0}'"
                try:
                    my_cursor.execute(sql3.format(placa_entry.get()))
                    mydb.commit()
                    #conn.close()
                    #my_cursor.execute(sql2.format(codigo_marca.get()))
                    #mydb.commit()
                    #conn.close()
                    #my_cursor.execute(sql.format(codigo_marca.get()))
                    #mydb.commit()
                    titulo = 'Ingresión'
                    mensaje = 'Vehiculo eliminado con exito'
                    messagebox.showinfo(titulo, mensaje)
                except:
                    titulo = 'Alquilado'
                    mensaje = 'Ocurrio un problema'
                    messagebox.showinfo(titulo, mensaje)
                finally:
                     actualizar_tree()

            def select_record(e):
                codigo_marca.delete(0,END)
                #nombre_marca.delete(0,END)
                #nombre_modelo.delete(0,END)
                placa_entry.delete(0,END)
                color_entry.delete(0,END)
                año_entry.delete(0,END)

                selected = my_tree.focus()
                values = my_tree.item(selected,'values')

                codigo_marca.insert(0,values[0])
                #nombre_marca.insert(0, values[1])
                #nombre_modelo.insert(0, values[2])
                placa_entry.insert(0, values[1])
                color_entry.insert(0, values[4])
                año_entry.insert(0, values[5])
                


            cod_marca = CTkLabel(frame_entry, text="Codigo")
            cod_marca.pack()
            codigo_marca = CTkEntry(frame_entry, fg_color="#003d3c", border_color="#00bfae")
            codigo_marca.pack(padx=15)

            placa_label = CTkLabel(frame_entry, text="Placa")
            placa_label.pack()
            placa_entry = CTkEntry(frame_entry, fg_color="#003d3c", border_color="#00bfae")
            placa_entry.pack()

            color_label = CTkLabel(frame_entry, text="Color")
            color_label.pack()
            color_entry = CTkEntry(frame_entry, fg_color="#003d3c", border_color="#00bfae")
            color_entry.pack()

            año_label = CTkLabel(frame_entry, text="Año")
            año_label.pack()
            año_entry = CTkEntry(frame_entry, fg_color="#003d3c", border_color="#00bfae")
            año_entry.pack()

            agreg = CTkButton(frame_entry, text="Agregar", command=agregar, fg_color="#003d3c")
            agreg.pack(pady=20)

            delete = CTkButton(frame_entry, text="Eliminar", command=eliminar,fg_color="#003d3c")
            delete.pack()

            marca = CTkButton(frame_entry, text="Registrar nueva marca", command=vehiculo_marca, fg_color="#005954")
            marca.pack(pady=20)

            tree_frame_master = Frame(self.root)
            tree_frame_master.pack(pady=20)

            tree_frame1 = Frame(self.root)
            tree_frame1.pack(pady=20)

            tree_scroll = Scrollbar(tree_frame1)
            tree_scroll.pack(side=RIGHT,fill=Y)

            bara = Scrollbar(tree_frame1, orient=HORIZONTAL)
            bara.pack(side=BOTTOM,fill=X)

            my_tree = ttk.Treeview(tree_frame1, yscrollcommand=tree_scroll.set, xscrollcommand=bara.set, selectmode="extended",show="headings")
            my_tree.pack()

            tree_scroll.config(command=my_tree.yview)
            bara.config(command=my_tree.xview)

            #CREACION DE COLUMNAS
            my_tree['columns']=("ID","Placa","Marca","Modelo","Color", "Año")

            my_tree.column("ID",anchor=CENTER,width=140)
            my_tree.column("Placa",anchor=CENTER,width=140)
            my_tree.column("Marca",anchor=CENTER,width=140)
            my_tree.column("Modelo",anchor=CENTER,width=140)
            my_tree.column("Color",anchor=CENTER,width=140)
            my_tree.column("Año",anchor=CENTER,width=140)

            my_tree.heading("ID", text="COD",anchor=CENTER)
            my_tree.heading("Placa", text="Placa",anchor=CENTER)
            my_tree.heading("Marca", text="Vehiculo Marca",anchor=CENTER)
            my_tree.heading("Modelo", text="Vehiculo Modelo",anchor=CENTER)
            my_tree.heading("Color", text="Color",anchor=CENTER)
            my_tree.heading("Año", text="Año",anchor=CENTER)
                    

            my_tree.tag_configure('oddrow', background="white")
            my_tree.tag_configure('evenrow', background="#5dc1b9")

            my_tree.bind("<ButtonRelease-1>", select_record)

            query_db()

            self.root.mainloop()
    Datos()
insertar()