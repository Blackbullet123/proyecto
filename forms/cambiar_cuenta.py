from customtkinter import *
from tkinter import *
from tkinter import messagebox
import sqlite3
import bcrypt


class VentanaCambiarUsuario(CTkToplevel):
    db_name = 'database_proyecto.db'

    def __init__(self, ventana_principal):
        super().__init__()

        self.ventana_principal = ventana_principal

        self.title("Cambiar usuario")
        self.geometry("350x300+550+250")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()

        frame = CTkFrame(self)
        frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        CTkLabel(frame, text="Iniciar sesión", text_color=("#00501B", "#00FF7F"), font=("Ubuntu", 22, "bold")).pack(pady=(0, 20))

        CTkLabel(frame, text="Usuario").pack(anchor="w")
        self.entry_usuario = CTkEntry(frame, placeholder_text="Ingrese usuario")
        self.entry_usuario.pack(fill=X, pady=5)

        CTkLabel(frame, text="Contraseña").pack(anchor="w", pady=(10, 0))
        self.entry_password = CTkEntry(frame, placeholder_text="Ingrese contraseña", show="*")
        self.entry_password.pack(fill=X, pady=5)

        frame_btn = CTkFrame(frame, fg_color="transparent")
        frame_btn.pack(pady=20, fill=X)

        CTkButton(frame_btn, text="Ingresar", fg_color="#00501B", command=self.Login).pack(side=LEFT, expand=True, padx=5)
        CTkButton(frame_btn, text="Cancelar", fg_color="#8B0000", command=self.destroy).pack(side=RIGHT, expand=True, padx=5)

    def Validar_formulario_completo(self):
        if self.entry_usuario.get() and self.entry_password.get():
            return True
        messagebox.showerror("ERROR", "Ingrese usuario y contraseña")
        return False

    def Validar_login(self, usuario, password):
        import sqlite3, bcrypt
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT Contraseña FROM Usuarios WHERE Usuario = ?", (usuario,))
            resultado = cursor.fetchone()
        if not resultado:
            return False
        contraseña_hash = resultado[0].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), contraseña_hash)

    def Validar_login_2(self, usuario, password):
        import sqlite3
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios_2 WHERE Usuario = ? AND Contraseña = ?", (usuario, password))
            return cursor.fetchone() is not None

    def Login(self):
        if not self.Validar_formulario_completo():
            return

        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        try:
            if self.Validar_login_2(usuario, password):
                from forms.master_usuario_2 import usuario
                messagebox.showinfo("BIENVENIDO", "Datos correctos")
                self.destroy()
                self.ventana_principal.root.destroy()
                usuario()

            elif self.Validar_login(usuario, password):
                from forms.form_master import Principal
                messagebox.showinfo("BIENVENIDO", "Datos correctos")
                self.destroy()
                self.ventana_principal.root.destroy()
                Principal()

            else:
                messagebox.showerror("ERROR", "Usuario o contraseña incorrectos")

        except sqlite3.Error as e:
            messagebox.showerror("ERROR BD", str(e))
