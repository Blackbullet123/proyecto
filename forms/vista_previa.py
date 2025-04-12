import io
import fitz
from PIL import Image, ImageTk
import tkinter as tk
import os
from customtkinter import *

def vista_previa_1():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    imagen_bytes = previsualizar_pdf("PDF\datos de vehiculos detallado.pdf")

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    #root.geometry("600x300")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_1(): 
        os.startfile(f"PDF\datos de vehiculos detallado.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_1()),corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()
    
def vista_previa_2():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    imagen_bytes = previsualizar_pdf("PDF\Vehiculos.pdf")

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    #root.geometry("600x300")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_2(): 
        os.startfile(f"PDF\Vehiculos.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_2()),corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()

    
def vista_previa_3():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    imagen_bytes = previsualizar_pdf("PDF\Todos los alquilados.pdf")

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    #root.geometry("600x300")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_3(): 
        os.startfile(f"PDF\Todos los alquilados.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_3()),corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,corner_radius=15, 
                                           text_color="black",width=90,height=40,cursor='hand2',
                                           border_color="lightgreen",border_width=2,
                                        fg_color="seagreen",hover_color="#57bd9e", font=("Helvetica", 18))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()
    