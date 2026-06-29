import csv as csv
import time as time
import subprocess as sp
import pandas as pd
import numpy as np
import requests
from datetime import date
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
import psutil

# VARIABLES


rutaorigen = "data/raw/" # Carpeta de origen; desde aquí se validan los datos
rutadestino = "data/validated/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.
archivocuentas = "datos_cuentas.csv"
archivotransaccion = "datos_transaccion.csv"
archivolibro = "datos_libro.csv"
datacuentas = [] # Tabla que guarda los datos de cuenta en formato json
datatransaccion = [] # Tabla que guarda los datos de transaccion en formato json
datalibros = [] # Tabla que guarda los datos en libro formato json
endpoint = 'https://gestioniaapi.onrender.com/enviar-datos'

load_dotenv(find_dotenv())

apikey = os.getenv("PASSWORD_SUPABASE")

headers_api_cuenta = {
    "Schema": "silver",
    "Table": "cuenta",
    "apikey": apikey
}

headers_api_transaccion = {
    "Schema": "silver",
    "Table": "transaccion",
    "apikey": apikey
}

headers_api_libro = {
    "Schema": "silver",
    "Table": "libro",
    "apikey": apikey
}

psutil.cpu_percent(interval=None) # Inicio de consumo de CPU; siempre empieza en 0, por lo que se inicia sin print para medir el consumo luego

# Prints para mostrar las carpetas de origen y destino definidas en la consola
timestampstart = datetime.now().timestamp()
print(f'Tiempo de inicio limpieza: {datetime.fromtimestamp(timestampstart)}')
print(f"RUTA DE ORIGEN: {rutaorigen}")
print(f"RUTA DE DESTINO: {rutadestino}")

##### LIMPIEZA TABLA CUENTA
timestampread1 = datetime.now().timestamp()
print(f'Tiempo de inicio lectura de datos cuenta: {datetime.fromtimestamp(timestampread1)}')
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivocuentas)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivocuentas}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #1. Reemplaza tildes u otros caracteres con letras regulares, con iconv
    sp.run([f'iconv -t ASCII//TRANSLIT {rutadestino+'datos_cuentas.csv'} > temp.csv && mv temp.csv {rutadestino+'datos_prueba.csv'}'],shell=True)

    #2. Reemplaza espacios vacíos con "NULL" usando pandas:
    #r = Raw (indica que es un string en bruto, para evitar interpretar caracteres especiales)
    #^ = Inicio de línea
    #\s = Espacios vacíos (para evitar que interprete espacios sin contenido como no nulos)
    #* = Indica una o múltiples apariciones
    #$ = Fin de línea
    #np.nan = Reemplaza estos espacios con NaN (Not A Number), para el propósito de usar fillna
    #fillna = Reemplaza los NaN definidos con un string que diga NULL

    #Columna de moneda; reemplaza nulos con None
    df['moneda'] = df['moneda'].replace(r'^\s*$', np.nan, regex=True).fillna('N/A')
    #Columna de saldo; reemplaza nulos con 0
    df['saldo'] = df['saldo'].replace(r'^\s*$', np.nan, regex=True).fillna(0)
    #Columna de estado; reemplaza nulos con false
    df['estado'] = df['estado'].replace(r'^\s*$', np.nan, regex=True).fillna('false')

    #3. Check para campos con F o T (True y False) / Idealmente debe ajustarse a las columnas necesarias, para evitar conflictos con otras columnas, como por ejemplo género
    df['estado'] = df['estado'].replace({'f': 'False', 't': 'True'})

    try:
        df.to_csv(rutadestino+archivocuentas, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivocuentas} ha sido limpiado con éxito')
timestampreadend1 = datetime.now().timestamp()
print(f'Tiempo de fin lectura de datos cuenta: {datetime.fromtimestamp(timestampreadend1)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")

##### LIMPIEZA TABLA TRANSACCION
timestampread2 = datetime.now().timestamp()
print(f'Tiempo de inicio lectura de datos transaccion: {datetime.fromtimestamp(timestampread2)}')
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivotransaccion)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivotransaccion}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #1. Reemplaza tildes u otros caracteres con letras regulares, con iconv
    sp.run([f'iconv -t ASCII//TRANSLIT {rutadestino+'datos_transaccion.csv'} > temp.csv && mv temp.csv {rutadestino+'datos_prueba.csv'}'],shell=True)

    #2. Reemplaza espacios vacíos con "NULL" usando pandas

    #Columna de monto; reemplaza nulos con 0
    df['monto'] = df['monto'].replace(r'^\s*$', np.nan, regex=True).fillna(0)
    #Columna de fecha; reemplaza nulos con el día en que se ejecuta el script
    df['fecha'] = df['fecha'].replace(r'^\s*$', np.nan, regex=True).fillna(date.today().isoformat())
    #Columna de estadotransaccion; reemplaza nulos con false
    df['estadotransaccion'] = df['estadotransaccion'].replace(r'^\s*$', np.nan, regex=True).fillna('False')

    #3. Check para campos con F o T (True y False) / Idealmente debe ajustarse a las columnas necesarias, para evitar conflictos con otras columnas, como por ejemplo género
    df['estadotransaccion'] = df['estadotransaccion'].replace({'f': 'False', 't': 'True'})

    try:
        df.to_csv(rutadestino+archivotransaccion, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivotransaccion} ha sido limpiado con éxito')
timestampreadend2 = datetime.now().timestamp()
print(f'Tiempo de fin lectura de datos transaccion: {datetime.fromtimestamp(timestampreadend2)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")

##### LIMPIEZA TABLA LIBRO
timestampread3 = datetime.now().timestamp()
print(f'Tiempo de inicio lectura de datos libro: {datetime.fromtimestamp(timestampread3)}')
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivolibro)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivolibro}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #1. Reemplaza tildes u otros caracteres con letras regulares, con iconv
    sp.run([f'iconv -t ASCII//TRANSLIT {rutadestino+'datos_libro.csv'} > temp.csv && mv temp.csv {rutadestino+'datos_prueba.csv'}'],shell=True)

    #2. Reemplaza espacios vacíos con "NULL" usando pandas

    #Columna de saldo; reemplaza nulos con 0
    df['saldo'] = df['saldo'].replace(r'^\s*$', np.nan, regex=True).fillna(0)
    #Columna de monto; reemplaza nulos con 0
    df['monto'] = df['monto'].replace(r'^\s*$', np.nan, regex=True).fillna(0)
    #Columna de fechalibro; reemplaza nulos con el día en que se ejecuta el script
    df['fechalibro'] = df['fechalibro'].replace(r'^\s*$', np.nan, regex=True).fillna(date.today().isoformat())

    try:
        df.to_csv(rutadestino+archivolibro, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivolibro} ha sido limpiado con éxito')
timestampreadend3 = datetime.now().timestamp()
print(f'Tiempo de fin lectura de datos libro: {datetime.fromtimestamp(timestampreadend3)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")

# SUBIDA A API
# Abre el archivo de cuentas y añade los datos a la lista "datacuentas"
timestampsend1 = datetime.now().timestamp()
print(f'Tiempo de inicio envío de datos cuenta: {datetime.fromtimestamp(timestampsend1)}')
with open(rutadestino+'datos_cuentas.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idcuenta']
        datacuentas.append(i)

##### ENVÍO TABLA CUENTA
try:
    print("ENVIANDO DATOS A TABLA CUENTA EN SILVER")
    respuesta = requests.post(endpoint, json=datacuentas, headers=headers_api_cuenta,timeout=10)

    respuesta.raise_for_status()

    print("Datos recibidos y subidos a la base de datos")
    print("Código:", respuesta.status_code)
    print("Respuesta del servidor:", respuesta.json())

except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Error de Tiempo de Espera (Timeout): {errt}")
except requests.exceptions.RequestException as err:
    print(f"Algo salió mal: {err}")

    # Abre el archivo de transacciones y añade los datos a la lista "datatransaccion"
with open(rutadestino+'datos_transaccion.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idtransaccion']
        datatransaccion.append(i)

timestampsendfin1 = datetime.now().timestamp()
print(f'Tiempo de fin envío de datos cuenta: {datetime.fromtimestamp(timestampsendfin1)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")

##### ENVÍO TABLA TRANSACCION
timestampsend2 = datetime.now().timestamp()
print(f'Tiempo de inicio envío de datos transaccion: {datetime.fromtimestamp(timestampsend2)}')
try:
    print("ENVIANDO DATOS A TABLA TRANSACCION EN SILVER")
    respuesta = requests.post(endpoint, json=datatransaccion, headers=headers_api_transaccion,timeout=10)

    respuesta.raise_for_status()

    print("Datos recibidos y subidos a la base de datos")
    print("Código:", respuesta.status_code)
    print("Respuesta del servidor:", respuesta.json())

except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Error de Tiempo de Espera (Timeout): {errt}")
except requests.exceptions.RequestException as err:
    print(f"Algo salió mal: {err}")

timestampsendfin2 = datetime.now().timestamp()
print(f'Tiempo de fin envío de datos transaccion: {datetime.fromtimestamp(timestampsendfin2)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")

##### ENVÍO TABLA LIBRO
timestampsend3 = datetime.now().timestamp()
print(f'Tiempo de inicio envío de datos libro: {datetime.fromtimestamp(timestampsend3)}')
# Abre el archivo de libro y añade los datos a la lista "datatransaccion"
with open(rutadestino+'datos_libro.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idlibro']
        datalibros.append(i)

try:
    print("ENVIANDO DATOS A TABLA LIBRO EN SILVER")
    respuesta = requests.post(endpoint, json=datalibros, headers=headers_api_libro,timeout=10)

    respuesta.raise_for_status()

    print("Datos recibidos y subidos a la base de datos")
    print("Código:", respuesta.status_code)
    print("Respuesta del servidor:", respuesta.json())

except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Error de Tiempo de Espera (Timeout): {errt}")
except requests.exceptions.RequestException as err:
    print(f"Algo salió mal: {err}")
timestampsendfin3 = datetime.now().timestamp()
print(f'Tiempo de fin envío de datos libro: {datetime.fromtimestamp(timestampsendfin3)}')

timestampend = datetime.now().timestamp()
print(f'Tiempo de fin limpieza: {datetime.fromtimestamp(timestampend)}')

### CHECKPOINT DE CONSUMO DE CPU Y RAM
print(f'USO DE CPU DEL SISTEMA: {psutil.cpu_percent(interval=None)}%')
ram_info = psutil.virtual_memory()
print(f"USO DE RAM DEL SISTEMA: {ram_info.used / (1024**3):.2f}/{ram_info.total / (1024**3):.2f} GB")