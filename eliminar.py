import os
import time
import datetime

# RUTA DE LA CARPETA A LIMPIAR (CAMBIA ESTO)
CARPETA_OBJETIVO = r"\\desktop-lq00sbp\Scanner"

# Obtener la fecha actual
hoy = datetime.datetime.today()

# Calcular la fecha límite (dos meses antes)
limite_fecha = hoy.replace(day=1) - datetime.timedelta(days=1)
limite_fecha = limite_fecha.replace(day=1)  # Primer día del mes de hace dos meses

# Recorrer los archivos de la carpeta
for archivo in os.listdir(CARPETA_OBJETIVO):
    ruta_completa = os.path.join(CARPETA_OBJETIVO, archivo)
    
    # Verificar si es un archivo
    if os.path.isfile(ruta_completa):
        # Obtener la fecha de modificación del archivo
        timestamp_mod = os.path.getmtime(ruta_completa)
        fecha_mod = datetime.datetime.fromtimestamp(timestamp_mod)

        # Si el archivo es más antiguo que el límite, eliminarlo
        if fecha_mod < limite_fecha:
            try:
                os.remove(ruta_completa)
                print(f"Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"No se pudo eliminar {archivo}: {e}")

print("Proceso de limpieza completado.")