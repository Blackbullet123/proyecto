from customtkinter import *
from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import datetime
import os
import platform

class FrameBackup(CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color='#EEEEEE')
        self.controlador = controlador

        HOST = "localhost"
        USUARIO = "root"
        port = "3306"
        CONTRASENA = "123456"
        BASEDATOS = "control_alquiler_Reych"
        ARCHIVO_HISTORIAL = "historial_backup.txt"


        def guardar_historial(tipo):
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            historial = cargar_historial()
            historial[tipo] = fecha_hora

            with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
                for clave, valor in historial.items():
                    f.write(f"{clave}={valor}\n")

            actualizar_labels()


        def cargar_historial():
            historial = {"backup": "No registrado", "restore": "No registrado"}

            if os.path.exists(ARCHIVO_HISTORIAL):
                with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                    for linea in f:
                        if "=" in linea:
                            clave, valor = linea.strip().split("=", 1)
                            if clave in historial:
                                historial[clave] = valor
            else:
                with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
                    f.write("backup=No registrado\nrestore=No registrado\n")

            return historial


        def actualizar_labels():
            historial = cargar_historial()
            lbl_ultimo_backup.config(text=f"🟢 Último Backup: {historial['backup']}")
            lbl_ultimo_restore.config(text=f"🔵 Último Restore: {historial['restore']}")



        def seleccionar_carpeta_backup():
            ruta = filedialog.askdirectory(title="Seleccionar carpeta para guardar backup")
            if ruta:
                entry_backup.delete(0, tk.END)
                entry_backup.insert(0, ruta)


        def seleccionar_archivo_restore():
            ruta = filedialog.askopenfilename(
                title="Seleccionar archivo de backup",
                filetypes=[("SQL files", "*.sql"), ("Todos los archivos", "*.*")]
            )
            if ruta:
                entry_restore.delete(0, tk.END)
                entry_restore.insert(0, ruta)


        def realizar_backup():
            ruta_backup = entry_backup.get()
            if not ruta_backup:
                messagebox.showwarning("Atención", "Debes seleccionar o escribir una carpeta para guardar el backup.")
                return

            fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"backup_{BASEDATOS}_{fecha_hora}.sql"
            ruta_completa = os.path.join(ruta_backup, nombre_archivo)

            try:
                sistema_operativo = platform.system()
                
                if sistema_operativo == "Windows":
                    rutas_posibles = [
                        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
                        r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe",
                        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
                        r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysqldump.exe",
                    ]
                    
                    mysqldump_path = None
                    for ruta in rutas_posibles:
                        if os.path.exists(ruta):
                            mysqldump_path = ruta
                            break
                    
                    if not mysqldump_path:
                        mysqldump_path = "mysqldump.exe"
                        
                else:
                    mysqldump_path = "mysqldump"

                comando = [
                    mysqldump_path,
                    f"-h{HOST}",
                    f"-P{port}",
                    f"-u{USUARIO}",
                    f"--password={CONTRASENA}",
                    BASEDATOS,
                ]

                with open(ruta_completa, "wb") as archivo:
                    resultado = subprocess.run(comando, stdout=archivo, stderr=subprocess.PIPE)

                if resultado.returncode == 0:
                    messagebox.showinfo("Éxito", f"✅ Backup creado en:\n{ruta_completa}")
                    guardar_historial("backup")
                else:
                    error_msg = resultado.stderr.decode('utf-8') if resultado.stderr else "Error desconocido"
                    messagebox.showerror("Error", f"Error al crear backup:\n{error_msg}")

            except Exception as e:
                messagebox.showerror("Error", f"Excepción inesperada:\n{str(e)}")


        def restaurar_backup():
            archivo_sql = entry_restore.get()
            if not archivo_sql:
                messagebox.showwarning("Atención", "Debes seleccionar o escribir el archivo de backup.")
                return

            if not os.path.exists(archivo_sql):
                messagebox.showerror("Error", "El archivo seleccionado no existe.")
                return

            confirmar = messagebox.askyesno("Confirmar", "¿Deseas restaurar este backup?\nEsto puede sobrescribir datos existentes.")
            if not confirmar:
                return

            try:
                sistema_operativo = platform.system()
                
                if sistema_operativo == "Windows":
                    rutas_posibles = [
                        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
                        r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
                        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
                        r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysql.exe",
                    ]
                    
                    mysql_path = None
                    for ruta in rutas_posibles:
                        if os.path.exists(ruta):
                            mysql_path = ruta
                            break
                    
                    if not mysql_path:
                        mysql_path = "mysql.exe"
                        
                else:
                    mysql_path = "mysql"

                comando_crear = [
                    mysql_path,
                    f"-h{HOST}",
                    f"-P{port}",
                    f"-u{USUARIO}",
                    f"--password={CONTRASENA}",
                    "-e",
                    f"CREATE DATABASE IF NOT EXISTS {BASEDATOS};"
                ]
                subprocess.run(comando_crear, stderr=subprocess.PIPE)

                comando_restore = [
                    mysql_path,
                    f"-h{HOST}",
                    f"-P{port}",
                    f"-u{USUARIO}",
                    f"--password={CONTRASENA}",
                    BASEDATOS,
                ]

                with open(archivo_sql, "rb") as archivo:
                        resultado = subprocess.run(comando_restore, stdin=archivo, stderr=subprocess.PIPE)

                        if resultado.returncode == 0:
                            messagebox.showinfo("Éxito", f"✅ Base de datos '{BASEDATOS}' restaurada desde:\n{archivo_sql}")
                            guardar_historial("restore")
                        else:
                            messagebox.showerror("Error", f"Error al restaurar backup:\n{resultado.stderr.decode('utf-8')}")

            except Exception as e:
                messagebox.showerror("Error", f"Excepción inesperada:\n{str(e)}")



        self.frame_main = CTkFrame(self, fg_color="#EEEEEE")
        self.frame_main.pack(fill=BOTH, expand=True)              

        frame_superior = CTkFrame(self.frame_main, fg_color="#EEEEEE")
        frame_superior.pack(pady=10, fill=X, expand=True, side="top")

        volver = CTkButton(frame_superior, text="← Volver", fg_color="#0E0F0F", cursor="hand2", text_color="white",
                           width=100, height=40)
        volver.pack(pady=10, padx=20, side=LEFT)

        titulo = CTkLabel(frame_superior, text="Backup & Restore",
                        text_color="#00501B", font=("Impact", 45))
        titulo.pack(pady=0, padx=60 ,side=RIGHT)

        frame_principal = Frame(self.frame_main, bg="#EEEEEE")
        frame_principal.pack(fill=BOTH, expand=True, anchor="center")

        frame_inferior = Frame(self.frame_main, bg="#EEEEEE")
        frame_inferior.pack(fill="x", expand=True)

        frame_backup_contenedor = CTkFrame(frame_principal,fg_color="#EEEEEE")
        frame_backup_contenedor.pack(fill="x", expand=True,pady=10, padx=20)

        frame_backup = tk.LabelFrame(frame_backup_contenedor, text="Crear Backup", font=("Arial", 12, "bold"), padx=10, pady=10)
        frame_backup.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_backup, text="Carpeta destino:", font=("Arial", 11)).pack(anchor="w")

        frame_ruta_backup = tk.Frame(frame_backup)
        frame_ruta_backup.pack(fill="x", pady=5)

        entry_backup = CTkEntry(frame_ruta_backup, font=("Arial", 10))
        entry_backup.pack(side="left", fill="x", expand=True, padx=5)

        btn_examinar_backup = CTkButton(frame_ruta_backup, text="Examinar", text_color="white", fg_color="black", width=10, command=seleccionar_carpeta_backup)
        btn_examinar_backup.pack(side="right", padx=5)

        btn_backup = CTkButton(frame_backup, text="Realizar Backup", text_color="white",font=("Arial", 12, "bold"), fg_color="#00501B", command=realizar_backup)
        btn_backup.pack(pady=10)

        frame_restore_contenedor = CTkFrame(frame_principal, fg_color="#EEEEEE")
        frame_restore_contenedor.pack(expand=True, fill="x", pady=10, padx=20)

        frame_restore = tk.LabelFrame(frame_restore_contenedor, text="Restaurar Backup",font=("Arial", 12, "bold"), padx=10, pady=10)
        frame_restore.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_restore, text="Archivo .sql:", font=("Arial", 11)).pack(anchor="w")

        frame_ruta_restore = tk.Frame(frame_restore)
        frame_ruta_restore.pack(fill="x", pady=5)

        entry_restore = CTkEntry(frame_ruta_restore, font=("Arial", 10))
        entry_restore.pack(side="left", fill="x", expand=True, padx=5)

        btn_examinar_restore = CTkButton(frame_ruta_restore, text="Examinar", text_color="white",width=10,fg_color="black", command=seleccionar_archivo_restore)
        btn_examinar_restore.pack(side="right", padx=5)

        btn_restore = CTkButton(frame_restore, text="Restaurar Backup", text_color="white",font=("Arial", 12,"bold"), fg_color="#00501B", command=restaurar_backup)
        btn_restore.pack(pady=10)

        frame_inferior_cont = CTkFrame(frame_inferior, corner_radius=15, fg_color="#EEEEEE")
        frame_inferior_cont.pack(expand=True, fill="x", pady=10, padx=20)

        frame_historial = tk.LabelFrame(frame_inferior_cont,text="Historial de operaciones", font=("Arial", 12, "bold"), padx=10, pady=10)
        frame_historial.pack(padx=20, pady=10, fill="x")

        lbl_ultimo_backup = tk.Label(frame_historial, text="", font=("Arial", 10))
        lbl_ultimo_backup.pack(anchor="w", pady=2)

        lbl_ultimo_restore = tk.Label(frame_historial, text="", font=("Arial", 10))
        lbl_ultimo_restore.pack(anchor="w", pady=2)

        actualizar_labels()


