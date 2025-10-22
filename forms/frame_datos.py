from customtkinter import *
from customtkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image

class FrameDatosDetallados(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='white')
        self.controlador = controlador

        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True)

        titulo = CTkLabel(frame_superior, text="DATOS DETALLADOS",
                        text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        boton_volver = CTkButton(self, text="Volver",
                                 fg_color="#0E0F0F", text_color="white",
                                 width=100, height=30
                                )
        boton_volver.pack(pady=20)