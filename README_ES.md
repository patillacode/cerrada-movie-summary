# Script de Resumen

Este script se utiliza para extraer datos de una URL dada y escribir los datos en un archivo.

## Instalación

1. Clona el repositorio.
2. Navega al directorio del proyecto.
3. Ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
make install
```

## Uso

Para ejecutar el script, usa el siguiente comando:

```bash
make run
```

Cuando se te solicite, introduce la URL de la película.

El script extraerá los datos y los escribirá en un archivo en el directorio `sumarios`. El archivo llevará el nombre del título de la película y contendrá el título, los nombres del reparto y el director.

## Limpieza

Para limpiar los archivos generados, usa el siguiente comando:

```bash
make clean
```
