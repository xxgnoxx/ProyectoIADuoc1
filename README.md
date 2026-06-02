# ProyectoIADuoc1
Repositorio para trabajo remoto para el proyecto de Gestión de datos de IA

# Estructura
datos_nuevos = Carpeta de origen para recibir datos y copiarlos. Los datos guardados aquí no se subirán al repositorio.
data/raw/ = Carpeta de destino para datos crudos copiados.
ingesta/ = Carpeta con script de ingesta, para compilar en un contenedor
script_ingesta.py = Script usado para copiar datos desde la carpeta de origen a la carpeta de destino, reemplazando los existentes.
limpíeza/ = Carpeta con script de limpíeza, para compilar en un contenedor
script_limpieza.py = Script para la limpieza de datos, basado en los datos en la carpeta raw.
validacion/ = Carpeta con script de validacion, para compilar en un contenedor
script_validacion.py = Script para validar los datos, arreglando datos nulos y formatos, basado en la carpeta validated.
.gitignore = Archivos ignorados.
docker-compose.yml = Archivo para separar scripts en múltiples contenedores Docker

# Instrucciones de instalación
1. Clonar el repositorio (git clone https://github.com/xxgnoxx/ProyectoIADuoc1)
