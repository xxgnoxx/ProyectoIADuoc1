import shutil as sh
import csv as csv
import time as time
import pandas as pd
import requests
from datetime import date

# VARIABLES


rutaorigen = "data/validated/" # Carpeta de origen; desde aquí se validan los datos
rutadestino = "data/curated/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.
archivocuentas = "datos_cuentas.csv"
archivotransaccion = "datos_transaccion.csv"
archivolibro = "datos_libro.csv"
datacuentas = [] # Tabla que guarda los datos de cuenta en formato json
datatransaccion = [] # Tabla que guarda los datos de cuenta en formato json
datalibros = [] # Tabla que guarda los datos en libro formato json
endpoint = 'https://gestioniaapi.onrender.com/enviar-datos'

headers_api_cuenta = {
    "Schema": "gold",
    "Table": "cuenta"
}

headers_api_transaccion = {
    "Schema": "gold",
    "Table": "transaccion"
}

headers_api_libro = {
    "Schema": "gold",
    "Table": "libro"
}

# Prints para mostrar las carpetas de origen y destino definidas en la consola
print(f"RUTA DE ORIGEN: {rutaorigen}")
print(f"RUTA DE DESTINO: {rutadestino}")


##### TABLA CUENTA
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivocuentas)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivocuentas}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #1. Revisa valores fuera de rango:
    #r = Raw (indica que es un string en bruto, para evitar interpretar caracteres especiales)
    #^ = Inicio de línea
    #\s = Espacios vacíos (para evitar que interprete espacios sin contenido como no nulos)
    #* = Indica una o múltiples apariciones
    #$ = Fin de línea

    #Columna de moneda; reemplaza valores None (acción hecha por el script de limpieza) con USD a manera de moneda por defecto
    df['moneda'] = df['moneda'].replace('N/A', 'USD')
    # Llena el espacio vacío que deja replace
    df['moneda'] = df['moneda'].fillna('USD')
    #Columna de saldo; si es menor a 0, lo reemplaza con 0
    df['saldo'] = df['saldo'].clip(0)

    try:
        df.to_csv(rutadestino+archivocuentas, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivocuentas} ha sido validado con éxito')


##### TABLA TRANSACCION
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivotransaccion)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivotransaccion}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #Columna de monto; si es menor que 0, se reemplaza con 0
    df['monto'] = df['monto'].clip(0)
    #Columna de fecha; si la fecha es después del día en que se ejecuta el script, se corrige a la fecha actual
    #Asegura que el tipo de dato sea correcto para pandas
    df['fecha'] = pd.to_datetime(df['fecha'])
    #Fecha de hoy
    today = pd.to_datetime('today').normalize()
    #Si es mayor, la reemplaza con el día de hoy
    df.loc[df['fecha'] > today, 'fecha'] = today

    #3. Check para campos con F o T (True y False) / Idealmente debe ajustarse a las columnas necesarias, para evitar conflictos con otras columnas, como por ejemplo género
    df['estadotransaccion'] = df['estadotransaccion'].replace({'f': 'False', 't': 'True'})

    try:
        df.to_csv(rutadestino+archivotransaccion, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivotransaccion} ha sido validado con éxito')


##### TABLA LIBRO
try:
    #Abre el archivo con pandas para editarlo con otras funciones
    df = pd.read_csv(rutaorigen+archivolibro)

# Si hay un error al abrir, hace un print con el error y el script se detiene
except Exception as errorprincipal:
    print(f'ERROR AL ABRIR ARCHIVO "{archivolibro}": {errorprincipal}')

# Si no hay un error, continúa
else:
    #Columna de saldo; si es menor que 0, se reemplaza con 0
    df['saldo'] = df['saldo'].clip(0)
    #Columna de monto; si es menor que 0, se reemplaza con 0
    df['monto'] = df['monto'].clip(0)
    #Columna de fechalibro; si la fecha es después del día en que se ejecuta el script, se corrige a la fecha actual
    #Asegura que el tipo de dato sea correcto para pandas
    df['fechalibro'] = pd.to_datetime(df['fechalibro'])
    #Fecha de hoy
    today = pd.to_datetime('today').normalize()
    #Si es mayor, la reemplaza con el día de hoy
    df.loc[df['fechalibro'] > today, 'fechalibro'] = today

    try:
        df.to_csv(rutadestino+archivolibro, index=False)
    except Exception as error:
        print(f'ERROR AL GUARDAR: {error}')
    else:
        print(f'El archivo {archivolibro} ha sido validado con éxito')


# SUBIDA A API
# Abre el archivo de cuentas y añade los datos a la lista "datacuentas"
with open(rutadestino+'datos_cuentas.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        datacuentas.append(i)



##### TABLA CUENTA
try:
    print("ENVIANDO DATOS A TABLA CUENTA EN GOLD")
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
        datatransaccion.append(i)

try:
    print("ENVIANDO DATOS A TABLA TRANSACCION EN GOLD")
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


##### TABLA LIBRO
# Abre el archivo de transacciones y añade los datos a la lista "datatransaccion"
with open(rutadestino+'datos_libro.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        datalibros.append(i)

try:
    print("ENVIANDO DATOS A TABLA LIBRO EN GOLD")
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