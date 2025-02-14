import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Ruta del archivo de configuración
config_path = os.path.join(os.path.expanduser("~"), "Documents", "Backups", "config.txt")

# Asegurar que la carpeta de backups exista
os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Verificar si existe el archivo de configuración
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        archivo_original = f.read().strip()
else:
    # Pedir la ruta del archivo con una ventana emergente
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo_original = filedialog.askopenfilename(title="Selecciona el archivo a respaldar")

    if not archivo_original:  # Si el usuario no selecciona nada, salir del programa
        messagebox.showwarning("Error", "No seleccionaste ningún archivo. El programa se cerrará.")
        exit()

    # Guardar la ruta en config.txt para futuras ejecuciones
    with open(config_path, "w") as f:
        f.write(archivo_original)

# Ruta de backup
carpeta_backup = os.path.join(os.path.expanduser("~"), "Documents", "Backups")
os.makedirs(carpeta_backup, exist_ok=True)

# Crear nombre con fecha
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_backup = os.path.join(carpeta_backup, f"backup_{fecha}.xlsm")

# Copiar archivo y mostrar mensaje
try:
    shutil.copy2(archivo_original, archivo_backup)
    messagebox.showinfo("Backup exitoso", f"Backup realizado correctamente en:\n{archivo_backup}")
except Exception as e:
    messagebox.showerror("Error", f"No se pudo realizar el backup:\n{e}")
