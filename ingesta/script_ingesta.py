import shutil as sh
import csv
import requests
from datetime import date

rutaorigen = "datos_nuevos" # Carpeta de origen; desde aquí se copian los datos
rutadestino = "data/raw/" # Carpeta destino; los datos de la carpeta origen se agregarán aquí. Archivos con nombres idénticos serán reemplazados.
datacuentas = [] # Tabla que guarda los datos de cuenta en formato json
datatransaccion = [] # Tabla que guarda los datos de cuenta en formato json
datalibros = [] # Tabla que guarda los datos en libro formato json
endpoint = 'https://gestioniaapi.onrender.com/enviar-datos'

headers_api_cuenta = {
    "Schema": "bronze",
    "Table": "cuenta"
}

headers_api_transaccion = {
    "Schema": "bronze",
    "Table": "transaccion"
}

headers_api_libro = {
    "Schema": "bronze",
    "Table": "libro"
}

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

##### TABLA CUENTA
with open(rutadestino+'datos_cuentas.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idcuenta']
        # Agrega datos vacíos al request; supabase no permite valores vacíos, por lo que se agregan valores vacíos como placeholder, mientras que el archivo se mantiene
        if (i['moneda'].strip()) == '':
            i['moneda'] = None
        if (i['saldo'].strip()) == '':
            i['saldo'] = None
        if (i['estado'].strip()) == '':
            i['estado'] = None
        datacuentas.append(i)



###### ENVÍO TABLA CUENTA
try:
    print("ENVIANDO DATOS A TABLA CUENTA EN BRONZE")
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

##### TABLA TRANSACCIÓN
with open(rutadestino+'datos_transaccion.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idtransaccion']
        # Agrega datos vacíos al request; supabase no permite valores vacíos, por lo que se agregan valores vacíos como placeholder, mientras que el archivo se mantiene
        if (i['monto'].strip()) == '':
            i['monto'] = None
        if (i['fecha'].strip()) == '':
            i['fecha'] = None
        if (i['estadotransaccion'].strip()) == '':
            i['estadotransaccion'] = None
        datatransaccion.append(i)

##### ENVÍO TABLA TRANSACCION
try:
    print("ENVIANDO DATOS A TABLA TRANSACCION EN BRONZE")
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
with open(rutadestino+'datos_libro.csv', encoding='UTF-8') as archivo:
    archivocsv = csv.reader(archivo, delimiter=',', quotechar='|')
    
    reader = csv.DictReader(archivo)

    for i in reader:
        del i['idlibro']
        # Agrega datos vacíos al request; supabase no permite valores vacíos, por lo que se agregan valores vacíos como placeholder, mientras que el archivo se mantiene
        if (i['saldo'].strip()) == '':
            i['saldo'] = None
        if (i['monto'].strip()) == '':
            i['monto'] = None
        if (i['fechalibro'].strip()) == '':
            i['fechalibro'] = None
        datalibros.append(i)

##### ENVÍO TABLA LIBRO
try:
    print("ENVIANDO DATOS A TABLA LIBRO EN BRONZE")
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