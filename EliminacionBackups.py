from datetime import datetime, timedelta
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import os

# Configuración
site_url = os.environ.get("SHAREPOINT_SITE_URL_2")
username = os.environ.get('REMITENTE')
password = os.environ.get('PASSWORD')
backup_folder = "Documentos compartidos/Backups"  # Carpeta principal donde están las subcarpetas de cada HPLC

if not site_url or not username or not password:
    print("Error: No se han configurado las credenciales de SharePoint.")
    exit()

# Conectar a SharePoint
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
main_folder = ctx.web.get_folder_by_server_relative_url(backup_folder)

# Obtener todas las subcarpetas (cada HPLC tiene una)
subfolders = main_folder.folders.get().execute_query()

# Fecha límite para eliminar backups (4 meses atrás)
fecha_limite = datetime.now() - timedelta(days=120)

print(f"Fecha límite para eliminación: {fecha_limite.strftime('%Y-%m-%d')}")

for subfolder in subfolders:
    folder_name = subfolder.properties["Name"]
    folder_path = f"{backup_folder}/{folder_name}"
    print(f"Revisando backups en {folder_name}...")

    # Obtener archivos en la subcarpeta
    files = subfolder.files.get().execute_query()

    for file in files:
        try:
            # Extraer la fecha del nombre (asumiendo formato: backup_HPLC_YYYY-MM-DD_HH-MM-SS.zip)
            fecha_str = file.properties["Name"].split("_")[1]
            fecha_archivo = datetime.strptime(fecha_str, "%Y-%m-%d")

            # Si el backup es más antiguo que la fecha límite, eliminarlo
            if fecha_archivo < fecha_limite:
                file.delete_object()
                ctx.execute_query()
                print(f"Eliminado: {file.properties['Name']} (creado el {fecha_archivo.strftime('%Y-%m-%d')})")
        except Exception as e:
            print(f"No se pudo eliminar {file.properties['Name']}: {e}")

print("Eliminación de backups antiguos completada.")
