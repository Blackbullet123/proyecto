import customtkinter as ctk  

# Inicialización de la aplicación  
ctk.set_appearance_mode("light")  # Puedes usar "dark" o "light"  
ctk.set_default_color_theme("blue")  

# Función para ajustar el ancho del CTkComboBox  
def ajustar_ancho(combobox):  
    opciones = combobox["values"]  
    # Calcular el ancho del texto más largo  
    max_width = max(len(opcion) for opcion in opciones) * 10  # Multiplica por 10 para ajustarlo  
    combobox.configure(width=max_width)  

# Crear la ventana principal  
ventana = ctk.CTk()  
ventana.title("Ejemplo de CTkComboBox")  
ventana.geometry("300x200")  

# Crear un CTkComboBox  
opciones = ["Opción 1", "Opción 2", "Opción 3 con texto largo", "Opción 4"]  
combobox = ctk.CTkComboBox(ventana, values=opciones)  
combobox.pack(pady=20)  

# Ajustar el ancho basado en las opciones  
ajustar_ancho(combobox)  

# Ejecutar la aplicación  
ventana.mainloop()  