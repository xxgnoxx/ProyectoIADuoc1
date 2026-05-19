import shutil as sh
import csv as csv
import time as time
import subprocess as sp

# VARIABLES


rutaorigen = "data/validated/" # Carpeta de origen; desde aquí se validan los datos
rutadestino = "data/curated/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.
lineas = [] # Lista para poder guardar los datos del csv y leerlos o editarlos de mejor manera

# Prints para mostrar las carpetas de origen y destino definidas en la consola
print(f"RUTA DE ORIGEN: {rutaorigen}")
print(f"RUTA DE DESTINO: {rutadestino}")

#Copia 
try:
    sh.copytree(rutaorigen, rutadestino, dirs_exist_ok=True)
    print("Datos copiados con éxito")
except Exception as texto_error:
    print(f"ERROR: {texto_error}")

#Abre el archivo
with open(rutadestino+'datos_prueba.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

#Comandos de linux:

#1. Reemplaza tildes u otros caracteres con letras regulares, con iconv en linux
sp.run([f'iconv -t ASCII//TRANSLIT {rutadestino+'datos_prueba.csv'} > temp.csv && mv temp.csv {rutadestino+'datos_prueba.csv'}'],shell=True)


#2. Reemplaza espacios vacíos con "NULL"
#df = pd.read_csv(rutadestino+'datos_prueba.csv')
#df = df.replace(r'^\s*$', np.nan, regex=True).fillna('NULL')
#print(df)
