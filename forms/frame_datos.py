from customtkinter import *

class FrameDatosDetallados(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='white')
        self.controlador = controlador

        label = CTkLabel(self, text="Pantalla de Datos Detallados",
                         text_color="black", font=("Ubuntu", 20))
        label.pack(pady=50)

        boton_volver = CTkButton(self, text="Volver",
                                 fg_color="#0E0F0F", text_color="white",
                                 width=100, height=30,
                                 command=self.controlador.mostrar_contenido_principal)
        boton_volver.pack(pady=20)
