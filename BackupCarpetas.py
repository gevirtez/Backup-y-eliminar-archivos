import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

# Obtener credenciales desde variables de entorno
site_url = os.environ.get("SHAREPOINT_SITE_URL_2")
username = os.environ.get('REMITENTE')
password = os.environ.get('PASSWORD')
sharepoint_folder = "Documentos compartidos/Backups/EDT 238"

if not site_url or not username or not password:
    messagebox.showerror("Error", "Las credenciales de SharePoint no están configuradas en las variables de entorno.")
    exit()

# Seleccionar la carpeta a respaldar
config_path = os.path.join(os.path.expanduser("~"), "Documents", "Backups", "config2.txt")
os.makedirs(os.path.dirname(config_path), exist_ok=True)

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        carpeta_origen = f.read().strip()
else:
    root = tk.Tk()
    root.withdraw()
    carpeta_origen = filedialog.askdirectory(title="Selecciona la carpeta a respaldar")
    if not carpeta_origen:
        messagebox.showwarning("Error", "No seleccionaste ninguna carpeta. El programa se cerrará.")
        exit()
    with open(config_path, "w") as f:
        f.write(carpeta_origen)

# Crear un archivo ZIP con la carpeta seleccionada
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_backup = os.path.join(os.path.expanduser("~"), f"backup_{fecha}.zip")
shutil.make_archive(archivo_backup[:-4], 'zip', carpeta_origen)

# Autenticación con usuario y contraseña usando variables de entorno
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

# Subir el archivo ZIP a SharePoint
with open(archivo_backup, "rb") as file_content:
    file_info = file_content.read()
    target_folder = ctx.web.get_folder_by_server_relative_url(sharepoint_folder)
    target_file = target_folder.upload_file(f"backup_{fecha}.zip", file_info)
    ctx.execute_query()

messagebox.showinfo("Backup exitoso", f"Backup subido correctamente a SharePoint en:\n{sharepoint_folder}")