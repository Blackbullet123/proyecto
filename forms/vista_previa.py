import io
import fitz
from PIL import Image, ImageTk
import tkinter as tk
import os
from customtkinter import *
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()
    
def vista_previa_1():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    pdf_path = get_project_root() / "PDF" / "datos de vehiculos detallado.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"El archivo {pdf_path} no existe.")
    imagen_bytes = previsualizar_pdf(pdf_path)

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    root.geometry("700x650+400+40")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_1(): 
        os.startfile(r"PDF\datos de vehiculos detallado.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_1()),
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14,"bold"))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14, "bold"))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()
    
def vista_previa_2():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    pdf_path = get_project_root() / "PDF" / "Vehiculos.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"El archivo {pdf_path} no existe.")
    imagen_bytes = previsualizar_pdf(pdf_path)

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    root.geometry("700x650+400+40")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_2(): 
        os.startfile(r"PDF\Vehiculos.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_2()),
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14,"bold"))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14, "bold"))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()

    
def vista_previa_3():
    
    def previsualizar_pdf(pdf_path):
        pdf = fitz.open(pdf_path)
        primera_pagina = pdf[0]
        imagen_bytes = primera_pagina.get_pixmap().tobytes()
        pdf.close()
        return imagen_bytes
    
    pdf_path = get_project_root() / "PDF" / "Todos los alquilados.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"El archivo {pdf_path} no existe.")
    imagen_bytes = previsualizar_pdf(pdf_path)

    root=tk.Toplevel()
    root.title("Imprimir")
    #root.configure(background='#2f7d55')
    root.geometry("700x650+400+40")
    image = Image.open(io.BytesIO(imagen_bytes))
    photo = ImageTk.PhotoImage(image.resize((700, 500)))

    label = tk.Label(root, image=photo)
    label.pack(padx=10, pady=5)
    titulo = tk.Label(root, text="¿Estás seguro que deseas exportar en PDF?", font=('Helvetica', 16), fg="black")
    titulo.pack(padx=10, pady=5)
    
    def open_pfd_3(): 
        os.startfile(r"PDF\Todos los alquilados.pdf")
    
    confirmar_boton = CTkButton(root,text="Confirmar",command=lambda: (root.destroy(), open_pfd_3()),
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14,"bold"))
    confirmar_boton.pack(padx=10,pady=3)
    
    cancelar_boton = CTkButton(root,text="Cancelar",command=root.destroy,
                                           text_color="white",cursor='hand2',
                                        fg_color="#00501B",hover_color="#57bd9e", font=("Arial", 14, "bold"))
    cancelar_boton.pack(padx=10,pady=3)
    root.mainloop()
    