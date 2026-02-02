from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
from forms.cambiar_cuenta import VentanaCambiarUsuario
import webbrowser
import os   
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class FrameConfiguracion(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador

        frame_superior = CTkFrame(self, fg_color="#EEEEEE")
        frame_superior.pack(fill=X, pady=10)


        titulo = CTkLabel(frame_superior,text="CONFIGURACIÓN",text_color="#00501B",font=("Impact", 45))
        titulo.pack(side=RIGHT, padx=60)

        self.contenedor = CTkFrame(self,fg_color="#F7F9FB",corner_radius=20)
        self.contenedor.pack(expand=True, fill="both", padx=60, pady=30)


        self.grid_botones = CTkFrame(self.contenedor, fg_color="transparent")
        self.grid_botones.pack(expand=True, fill="both", padx=120, pady=20)

        self.grid_botones.columnconfigure((0, 1), weight=1)
        self.grid_botones.rowconfigure((0, 1), weight=1)


        img = Image.open("imagenes/perfil.png")
        micuenta_icon = CTkImage(dark_image=img, light_image=img, size=(65,65))
        self.btn_micuenta = CTkButton(self.grid_botones,text="Mi Cuenta",font=("Ubuntu",20,"bold"),
                                        fg_color="#E9EEF3",hover_color="#D5DBE0",text_color="#1F2937",corner_radius=16,border_width=1,
                                    border_color="#E0E3E7",height=140, command=self.cambiar_cuenta,image=micuenta_icon, compound="top")
        self.btn_micuenta.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/backup.png")
        backup_icon = CTkImage(dark_image=img, light_image=img, size=(65,65))
        self.btn_backup = CTkButton(self.grid_botones,text="Backup & Restore",font=("Ubuntu",20,"bold"),fg_color="#E9EEF3",
                                    hover_color="#D5DBE0",text_color="#1F2937",corner_radius=16,border_width=1,
                            border_color="#E0E3E7",height=140,image=backup_icon, compound="top")
        self.btn_backup.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/ayuda.png")
        ayuda_icon = CTkImage(dark_image=img, light_image=img, size=(65,65))
        self.btn_ayuda =CTkButton(self.grid_botones,text="Ayuda",font=("Ubuntu",20,"bold"),fg_color="#E9EEF3",
                                        hover_color="#D5DBE0",text_color="#1F2937",corner_radius=16,border_width=1,
                                    border_color="#E0E3E7", command=abrir_pdf,height=140, image=ayuda_icon, compound="top")
        self.btn_ayuda.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/apariencia.png")
        apariencia_icon = CTkImage(dark_image=img, light_image=img, size=(65,65))
        self.btn_apariencia = CTkButton(self.grid_botones,text="Apariencia",font=("Ubuntu",20,"bold"),
                                        fg_color="#E9EEF3",hover_color="#D5DBE0",text_color="#1F2937",corner_radius=16,
                                    border_width=1,border_color="#E0E3E7",height=140, image=apariencia_icon, compound="top")
        self.btn_apariencia.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

    def cambiar_cuenta(self):
        ventana_cambiar_usuario = VentanaCambiarUsuario(self.controlador)


def abrir_pdf():
    ruta_pdf = get_project_root() / "PDF" / "manual.pdf"
    
    if os.path.exists(ruta_pdf):
        url_pdf = f"file://{ruta_pdf.absolute()}"
        webbrowser.open_new(url_pdf)

pdf_path = get_project_root() / "PDF" / "manual.pdf"        
ruta_pdf = pdf_path