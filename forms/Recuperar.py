import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

def abrir_ventana_secundaria():
    ventana_secundaria = ctk.CTkToplevel()
    ventana_secundaria.title("Ventana secundaria")
    ventana_secundaria.config(width=300, height=200)

    boton_cerrar = ctk.CTkButton(
        ventana_secundaria,
        text="Cerrar ventana", 
        command=ventana_secundaria.destroy
    )
    boton_cerrar.place(x=75, y=75)
ventana_principal = ctk.CTk()
ventana_principal.config(width=400, height=300)
ventana_principal.title("Ventana principal")

boton_abrir = ctk.CTkButton(
    ventana_principal,
    text="Abrir ventana secundaria",
    command=abrir_ventana_secundaria
)
boton_abrir.place(x=100, y=100)
ventana_principal.mainloop()