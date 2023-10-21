# Script de Web Scraping para IAFD

Este script está diseñado para extraer datos de películas de la Internet Adult Film Database (IAFD) a partir de una URL dada y escribir los datos en un archivo. Los datos incluyen el título de la película, los nombres del reparto y el director.

## Instalación

1. Clona el repositorio.
2. Navega al directorio del proyecto.
3. Ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
make install
```

## Uso

Hay dos formas de ejecutar el script:

### Terminal

Para ejecutar el script a través de la terminal, usa el siguiente comando:

```bash
make run
```

Cuando se te solicite, introduce la URL de la película. El script extraerá los datos y los escribirá en un archivo en el directorio `sumarios`. El archivo llevará el nombre del título de la película.

### GUI

Para ejecutar el script a través de la GUI, usa el siguiente comando:

```bash
make run-gui
```

En la GUI, introduce la URL de la película en el campo URL, especifica el directorio de destino y haz clic en el botón "Run Script". El script extraerá los datos y los escribirá en un archivo en el directorio especificado. El archivo llevará el nombre del título de la película.

La GUI también proporciona una opción para ejecutar el script en modo sin cabeza (sin abrir la ventana del navegador), y un botón para borrar la entrada de URL.

## Limpieza

Para limpiar los archivos generados, usa el siguiente comando:

```bash
make clean
```

Esto eliminará todos los archivos `.pyc`, los directorios `__pycache__`, el directorio `sumarios` y el entorno virtual.
