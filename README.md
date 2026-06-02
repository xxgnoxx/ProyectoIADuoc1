# ProyectoIADuoc1
Repositorio para trabajo remoto para el proyecto de Gestión de datos de IA

# Estructura
datos_nuevos = Carpeta de origen para recibir datos y copiarlos. Los datos guardados aquí no se subirán al repositorio.
data/raw/ = Carpeta de destino para datos crudos copiados.
script_ingesta.py = Script usado para copiar datos desde la carpeta de origen a la carpeta de destino, reemplazando los existentes.
script_limpieza.py = Script para la limpieza de datos, basado en los datos en la carpeta raw. No funcional por el momento.
script_validacion.py = Script para validar los datos, arreglando datos nulos y formatos. No funcional por el momento.
.gitignore = Archivos ignorados, en este caso cualquier dato dentro de la carpeta datos_nuevos para evitar copias.