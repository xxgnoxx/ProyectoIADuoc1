import shutil as sh

rutaorigen = "datos_nuevos/" # Carpeta de origen; desde aquí se copian los datos
rutadestino = "data/raw/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.

# Prints para mostrar las carpetas de origen y destino definidas en la consola
print(f"RUTA DE ORIGEN: {rutaorigen}")
print(f"RUTA DE DESTINO: {rutadestino}")

# Try/except en caso de errores:
# Si es exitoso, copia la carpeta origen a la carpeta destino, con un mensaje en la consola indicando que no hubo problemas
# Si hay un error, se muestra un mensaje con el error que ocurrió
try:
    sh.copytree(rutaorigen, rutadestino, dirs_exist_ok=True)
    print("Datos copiados con éxito")
except Exception as texto_error:
    print(f"ERROR: {texto_error}")