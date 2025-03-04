import os
import shutil
import requests
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Obtener carpeta de respaldo y carpeta de destino
config_path = os.path.join(os.path.expanduser("~"), "Documents", "Backups", "config2.txt")
os.makedirs(os.path.dirname(config_path), exist_ok=True)

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        lines = f.readlines()
        carpeta_origen = lines[0].strip()
        carpeta_destino = lines[1].strip() if len(lines) > 1 else ""
else:
    root = tk.Tk()
    root.withdraw()
    carpeta_origen = filedialog.askdirectory(title="Selecciona la carpeta a respaldar")
    if not carpeta_origen:
        messagebox.showwarning("Error", "No seleccionaste ninguna carpeta. El programa se cerrará.")
        exit()
    carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta de red donde guardar el backup")
    if not carpeta_destino:
        messagebox.showwarning("Error", "No seleccionaste ninguna carpeta de destino. El programa se cerrará.")
        exit()
    with open(config_path, "w") as f:
        f.write(f"{carpeta_origen}\n{carpeta_destino}")

# Crear archivo ZIP
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = os.path.join(os.path.expanduser("~"), "Documents", "Backups")
os.makedirs(backup_dir, exist_ok=True)
archivo_backup_sin_ext = os.path.join(backup_dir, f"backup_{fecha}")
archivo_backup = archivo_backup_sin_ext + ".zip"

shutil.make_archive(archivo_backup_sin_ext, 'zip', carpeta_origen)

# Verificar si el archivo fue creado correctamente
if not os.path.exists(archivo_backup):
    print(f"⚠️ ERROR: No se pudo encontrar el archivo ZIP en: {archivo_backup}")
    messagebox.showerror("Error", f"No se pudo crear el archivo ZIP en:\n{archivo_backup}")
    exit()

print(f"✅ Archivo ZIP creado en: {archivo_backup}")

# Copiar el archivo ZIP a la unidad de red
archivo_backup_red = os.path.join(carpeta_destino, os.path.basename(archivo_backup))
try:
    shutil.copy2(archivo_backup, archivo_backup_red)
    print(f"✅ Backup copiado a la unidad de red: {archivo_backup_red}")
except Exception as e:
    print(f"❌ ERROR al copiar el archivo a la unidad de red: {e}")
    messagebox.showerror("Error", f"No se pudo copiar el archivo a la unidad de red:\n{e}")

messagebox.showinfo("Backup exitoso", f"Backup guardado correctamente en:\n- {archivo_backup}\n- {archivo_backup_red}")
