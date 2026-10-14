
# ==================================================
# SISTEMA ACADEMICO
# Archivo: shared/json_manager.py
# ==================================================

# json nos permite leer y guardar datos en formato JSON.
import json

# os nos permite trabajar con archivos y carpetas.
import os


# Esta clase administra nuestros archivos JSON.
class GestorJSON:

    # Recibimos la ruta del archivo que utilizaremos.
    def __init__(self, archivo):

        # Guardamos la ruta dentro del objeto.
        self.archivo = archivo

    # ==============================================
    # LEER DATOS
    # ==============================================

    # Esta funcion obtiene los datos guardados.
    def leer(self):

        # Comprobamos si el archivo existe.
        if not os.path.exists(self.archivo):

            # Si no existe, devolvemos una lista vacia.
            return []

        # Abrimos el archivo en modo lectura ("r").
        with open(self.archivo, "r", encoding="utf-8") as archivo:

            # Convertimos el contenido JSON en datos de Python.
            datos = json.load(archivo)

            # Devolvemos los datos encontrados.
            return datos

    # ==============================================
    # GUARDAR DATOS
    # ==============================================

    # Esta funcion recibe la informacion que guardaremos.
    def guardar(self, datos):

        # Obtenemos el nombre de la carpeta del archivo.
        carpeta = os.path.dirname(self.archivo)

        # Si hay una carpeta, comprobamos que exista.
        if carpeta:

            # La creamos si todavia no existe.
            os.makedirs(carpeta, exist_ok=True)

        # Abrimos el archivo en modo escritura ("w").
        with open(self.archivo, "w", encoding="utf-8") as archivo:

            # Guardamos los datos en formato JSON.
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )
