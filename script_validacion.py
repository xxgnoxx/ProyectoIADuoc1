import shutil as sh
import csv as csv
import time as time

# VARIABLES


rutaorigen = "data/validated/" # Carpeta de origen; desde aquí se validan los datos
rutadestino = "data/curated/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.
lineas = [] # Lista para poder guardar los datos del csv y leerlos o editarlos de mejor manera
listainterna = [] # Lista para guardar valores de forma individual en la lista "lineas", en vez de un string completo

# Prints para mostrar las carpetas de origen y destino definidas en la consola
print(f"RUTA DE ORIGEN: {rutaorigen}")
print(f"RUTA DE DESTINO: {rutadestino}")

archivo = csv.reader(rutaorigen)
startappend = False

# COPIA DE DATOS PARA VALIDAR / PYTHON SOLO


# Try/except en caso de errores:
# Si es exitoso, copia la carpeta origen a la carpeta destino
# Si hay un error, se muestra un mensaje con el error que ocurrió
# Este archivo copiado a la carpeta "curated" será el utilizado para escanear y editar
try:
    sh.copytree(rutaorigen, rutadestino, dirs_exist_ok=True) # Copiar a la carpeta "curated" si no hay errores durante el proceso
except Exception as texto_error:
    print(f"ERROR: {texto_error}")

#with open(rutadestino+'datos_caso1_fintech.csv', encoding='UTF-8') as archivo:
#    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
#    reader = csv.DictReader(archivo)


#for i in range(len(lineas)):
#    print('Línea ' + str(i+1) + ': ' + str(lineas[i])) # Print debug: Imprime el número de la línea que está leyendo, y sus datos


# VALIDACIÓN