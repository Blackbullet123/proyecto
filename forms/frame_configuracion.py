from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
from forms.cambiar_cuenta import VentanaCambiarUsuario
from forms.frame_respaldo import FrameBackup
import webbrowser
import os   
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent if "__file__" in locals() else Path.cwd()

class FrameConfiguracion(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color=('#EEEEEE', '#1A1A1A'))

        self.controlador = controlador

        self.datos_conexion = {
            "host": "localhost",
            "user": "root",
            "password": "123456",
            "database": "control_alquiler_Reych",
            "port": "3306",
            "mysql_path": r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
        }


        frame_superior = CTkFrame(self, fg_color=("#EEEEEE", "#1A1A1A"))
        frame_superior.pack(fill=X, pady=10)



        titulo = CTkLabel(frame_superior,text="CONFIGURACIÓN",text_color=("#00501B", "#00FF7F"),font=("Impact", 45))
        titulo.pack(side=RIGHT, padx=60)


        self.contenedor = CTkFrame(self,fg_color=("#F7F9FB", "#2B2B2B"),corner_radius=20)
        self.contenedor.pack(expand=True, fill="both", padx=60, pady=30)



        self.grid_botones = CTkFrame(self.contenedor, fg_color="transparent")
        self.grid_botones.pack(expand=True, fill="both", padx=120, pady=20)

        self.grid_botones.columnconfigure((0, 1), weight=1)
        self.grid_botones.rowconfigure((0, 1), weight=1)


        img = Image.open("imagenes/perfil.png")
        img_white = Image.open("imagenes/perfil_white.png")
        micuenta_icon = CTkImage(light_image=img, dark_image=img_white, size=(65,65))
        self.btn_micuenta = CTkButton(self.grid_botones,text="Mi Cuenta",font=("Ubuntu",20,"bold"),
                                        fg_color=("#E9EEF3", "#333333"),hover_color=("#D5DBE0", "#444444"),text_color=("#1F2937", "#FFFFFF"),corner_radius=16,border_width=1,
                                    border_color=("#E0E3E7", "#444444"),height=140, command=self.cambiar_cuenta,image=micuenta_icon, compound="top")


        self.btn_micuenta.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/backup.png")
        img_white = Image.open("imagenes/backup_white.png")
        backup_icon = CTkImage(light_image=img, dark_image=img_white, size=(65,65))
        self.btn_backup = CTkButton(self.grid_botones,text="Backup & Restore",font=("Ubuntu",20,"bold"),fg_color=("#E9EEF3", "#333333"),
                                    hover_color=("#D5DBE0", "#444444"),text_color=("#1F2937", "#FFFFFF"),corner_radius=16,border_width=1,
                                    border_color=("#E0E3E7", "#444444"),height=140, command=self.abrir_backup,image=backup_icon,compound="top")


        self.btn_backup.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/ayuda.png")
        img_white = Image.open("imagenes/ayuda_white.png")
        ayuda_icon = CTkImage(light_image=img, dark_image=img_white, size=(65,65))
        self.btn_ayuda =CTkButton(self.grid_botones,text="Ayuda",font=("Ubuntu",20,"bold"),fg_color=("#E9EEF3", "#333333"),
                                        hover_color=("#D5DBE0", "#444444"),text_color=("#1F2937", "#FFFFFF"),corner_radius=16,border_width=1,
                                    border_color=("#E0E3E7", "#444444"), command=abrir_pdf,height=140, image=ayuda_icon, compound="top")

        self.btn_ayuda.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")


        img = Image.open("imagenes/apariencia.png")
        img_white = Image.open("imagenes/apariencia_white.png")
        apariencia_icon = CTkImage(light_image=img, dark_image=img_white, size=(65,65))
        self.btn_apariencia = CTkButton(self.grid_botones,text="Apariencia",font=("Ubuntu",20,"bold"),
                                        fg_color=("#E9EEF3", "#333333"),hover_color=("#D5DBE0", "#444444"),text_color=("#1F2937", "#FFFFFF"),corner_radius=16,
                                    border_width=1,border_color=("#E0E3E7", "#444444"),height=140, image=apariencia_icon, compound="top",
                                    command=self.cambiar_apariencia)


        self.btn_apariencia.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

    def cambiar_apariencia(self):
        if get_appearance_mode() == "Light":
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")
            
        # Notificar al controlador para actualizar gráficos inmediatamente
        if hasattr(self.controlador, 'actualizar_graficos_por_apariencia'):
            self.controlador.actualizar_graficos_por_apariencia()


    def cambiar_cuenta(self):
        ventana_cambiar_usuario = VentanaCambiarUsuario(self.controlador)

    def abrir_backup(self):
        ventana_backup = FrameBackup(self.controlador)



def abrir_pdf():
    ruta_pdf = get_project_root() / "PDF" / "manual.pdf"
    
    if os.path.exists(ruta_pdf):
        url_pdf = f"file://{ruta_pdf.absolute()}"
        webbrowser.open_new(url_pdf)

pdf_path = get_project_root() / "PDF" / "manual.pdf"        
ruta_pdf = pdf_path