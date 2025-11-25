from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
from forms.frame_respaldo import FrameBackup

class FrameConfiguracion(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador

        self.respaldo_frame = FrameBackup(self, controlador)

        self.frame_top = CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(side=TOP, fill=X, pady=10, padx=10)

        frame_botones = CTkFrame(self.frame_top, fg_color="transparent")
        frame_botones.pack(side=LEFT, fill=X)

        img = Image.open("imagenes/backup.png")
        backup_icon = CTkImage(dark_image=img, light_image=img, size=(40,40))
        backup_restore = CTkButton(frame_botones, text="Backup & Restore",fg_color="#00501B",cursor="hand2",text_color="white",
                                  width=170, height=170,hover_color="#008fa8",
                                  font=("Ubuntu",22), anchor=W, image=backup_icon, compound="top",
                                  command=self.mostrar_respaldo)
        backup_restore.pack(pady=5, padx=2, side=LEFT)


    def mostrar_respaldo(self):
        self.frame_top.pack_forget()
        self.respaldo_frame.pack(fill=BOTH, expand=True)