from customtkinter import *

class FrameVehiculos(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="white")
        self.controlador = controlador

        # ---- Frame superior ----
        self.frame_superior = CTkFrame(self, fg_color="#F0F0F0", corner_radius=10)
        self.frame_superior.pack(fill="x", padx=20, pady=10)

        CTkLabel(self.frame_superior, text="Buscar Vehículo:", text_color="black", font=("Ubuntu", 14)).pack(side="left", padx=5)
        self.entry_buscar = CTkEntry(self.frame_superior, width=250)
        self.entry_buscar.pack(side="left", padx=5)
        CTkButton(self.frame_superior, text="Buscar", fg_color="#0E0F0F", text_color="white", width=100,
                  command=self.buscar_vehiculo).pack(side="left", padx=10)

        # ---- Frame inferior ----
        self.frame_inferior = CTkFrame(self, fg_color="white")
        self.frame_inferior.pack(fill="both", expand=True, padx=20, pady=10)

        # Subframe para tabla u otros contenidos
        self.subframe_tabla = CTkFrame(self.frame_inferior, fg_color="#E8E8E8", corner_radius=10)
        self.subframe_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        CTkLabel(self.subframe_tabla, text="Aquí irá la tabla de vehículos", text_color="black").pack(pady=40)

    def buscar_vehiculo(self):
        print(f"Buscando vehículo: {self.entry_buscar.get()}")
