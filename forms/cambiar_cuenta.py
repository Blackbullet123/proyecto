from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

class VentanaCambiarUsuario(CTkToplevel):
    def __init__(self, controlador):
        super().__init__()

        self.controlador = controlador

        self.title("Cambiar usuario")
        self.geometry("350x300+350+150")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()

        frame = CTkFrame(self)
        frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        CTkLabel(frame,text="Iniciar sesión",font=("Ubuntu", 22, "bold")).pack(pady=(0, 20))

        CTkLabel(frame, text="Usuario").pack(anchor="w")
        self.entry_usuario = CTkEntry(frame, placeholder_text="Ingrese usuario")
        self.entry_usuario.pack(fill=X, pady=5)

        CTkLabel(frame, text="Contraseña").pack(anchor="w", pady=(10, 0))
        self.entry_password = CTkEntry(frame,placeholder_text="Ingrese contraseña",show="*")
        self.entry_password.pack(fill=X, pady=5)


        frame_btn = CTkFrame(frame, fg_color="transparent")
        frame_btn.pack(pady=20, fill=X)

        CTkButton(frame_btn,text="Ingresar",fg_color="#00501B").pack(side=LEFT, expand=True, padx=5)

        CTkButton(frame_btn,text="Cancelar",fg_color="#8B0000",command=self.destroy).pack(side=RIGHT, expand=True, padx=5)

