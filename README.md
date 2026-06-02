# ProyectoIADuoc1  
Repositorio para trabajo remoto para el proyecto de Gestión de datos de IA; contiene scripts para gestionar datos y enviarlos a la API.  

# Estructura  
├──datos_nuevos = Carpeta de origen para recibir datos y copiarlos. Los datos guardados aquí no se subirán al repositorio.  
├──data/curated/ = Carpeta de destino para datos copiados y validados con script_validacion.py.  
├──data/raw/ = Carpeta de destino para datos crudos copiados con script_ingesta.py.  
├──data/validated/ = Carpeta de destino para datos copiados y limpiados con script_limpieza.py.  
├──ingesta/ = Carpeta con script de ingesta, para compilar en un contenedor.  
│   ├──ingesta/script_ingesta.py = Script usado para copiar datos desde la carpeta de origen a la carpeta de destino, reemplazando los existentes.  
├──limpíeza/ = Carpeta con script de limpíeza, para compilar en un contenedor  
│   ├──limpíeza/script_limpieza.py = Script para la limpieza de datos, basado en los datos en la carpeta raw.  
├──validacion/ = Carpeta con script de validacion, para compilar en un contenedor  
│   ├──validacion/script_validacion.py = Script para validar los datos, arreglando datos nulos y formatos, basado en la carpeta validated.  
├──.gitignore = Archivos ignorados.  
├──docker-compose.yml = Archivo para separar scripts en múltiples contenedores Docker  

# Instrucciones de instalación  
1. Clonar el repositorio (git clone https://github.com/xxgnoxx/ProyectoIADuoc1)  
2. Revisar que la carpeta 'datos_nuevos' tenga los datos necesarios (incluidos en el repositorio)  
3. Asegurar que Docker Desktop esté instalado y ejecutado  
4. Instalar los contenedores usando 'docker_compose up' en la carpeta raíz del proyecto; alternativamente, usar 'docker_compose up -d' si no se necesita ver los logs  

# Desinstalación  
1. Ejecutar 'docker-compose down' en la carpeta raíz  
2. Eliminar la carpeta del proyecto  