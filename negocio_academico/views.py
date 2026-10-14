
# ==================================================
# SISTEMA ACADEMICO
# Archivo: views.py
# ==================================================

# ABC y abstractmethod permiten crear
# una clase abstracta.
from abc import ABC, abstractmethod

# Importamos la clase que lee y guarda JSON.
from shared.json_manager import GestorJSON

# Importamos funciones para mostrar mensajes.
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)


# ==================================================
# CLASE 1: CRUD BASE
# ==================================================

# CRUD significa:
# C = Create   (Crear)
# R = Read     (Leer)
# U = Update   (Actualizar)
# D = Delete   (Eliminar)
#
# Esta clase contiene las operaciones generales.
# Los controladores de nuestro sistema la heredaran.
# Asi no repetimos el mismo codigo cuatro veces.

class CrudBase(ABC):

    # La clase hija indicara que modelo utiliza.
    MODELO = None

    # La clase hija indicara su archivo JSON.
    ARCHIVO = ""

    # Nombre que mostraremos en los mensajes.
    NOMBRE = "registro"

    # Campos por los que se puede buscar.
    CAMPOS_BUSCABLES = ()

    # ==============================================
    # CONSTRUCTOR
    # ==============================================

    def __init__(self):

        # Creamos un gestor para el archivo JSON.
        self._gestor = GestorJSON(self.ARCHIVO)

    # ==============================================
    # LISTAR REGISTROS
    # ==============================================

    def listar(self):

        # Leemos los diccionarios del archivo JSON.
        datos = self._gestor.leer()

        # Aqui guardaremos los objetos recuperados.
        objetos = []

        # Recorremos cada diccionario guardado.
        for registro in datos:

            # Convertimos el diccionario en un objeto.
            objeto = self.MODELO.desde_diccionario(registro)

            # Agregamos el objeto a la lista.
            objetos.append(objeto)

        return objetos

    # ==============================================
    # GUARDAR REGISTROS
    # ==============================================

    def guardar(self, objetos):

        # JSON guarda diccionarios, no objetos Python.
        datos = []

        # Convertimos cada objeto en diccionario.
        for objeto in objetos:

            diccionario = objeto.a_diccionario()

            datos.append(diccionario)

        # Guardamos todos los registros.
        self._gestor.guardar(datos)

    # ==============================================
    # GENERAR EL SIGUIENTE ID
    # ==============================================

    def siguiente_id(self):

        objetos = self.listar()

        # Si no existen registros, empezamos en 1.
        if not objetos:
            return 1

        # Buscamos el ID mas grande.
        mayor = 0

        for objeto in objetos:

            if objeto.id > mayor:
                mayor = objeto.id

        # El siguiente sera uno mas.
        return mayor + 1

    # ==============================================
    # VALIDAR DATOS
    # ==============================================

    # Cada controlador tendra sus propias reglas.
    # Por ejemplo, no repetir un carnet o un correo.

    @abstractmethod
    def validar(self, datos, id_actual=None):
        pass

    # ==============================================
    # PREPARAR DATOS
    # ==============================================

    # Esta funcion permite ajustar los datos
    # antes de crear un objeto.
    # Por defecto no cambia nada.

    def preparar(self, datos):
        return datos

    # ==============================================
    # CREAR UN REGISTRO
    # ==============================================

    def crear(self, datos):

        # Hacemos una copia para no cambiar
        # el diccionario original.
        datos = datos.copy()

        # Preparamos los datos recibidos.
        datos = self.preparar(datos)

        # Comprobamos las reglas del controlador.
        self.validar(datos)

        # Generamos un ID nuevo.
        nuevo_id = self.siguiente_id()

        # Creamos el objeto con sus datos.
        nuevo = self.MODELO(nuevo_id, **datos)

        # Recuperamos los registros existentes.
        objetos = self.listar()

        # Agregamos el nuevo objeto.
        objetos.append(nuevo)

        # Guardamos toda la lista en JSON.
        self.guardar(objetos)

        return nuevo

    # ==============================================
    # BUSCAR UN REGISTRO POR ID
    # ==============================================

    def obtener(self, id_registro):

        # Comprobamos que el ID sea numerico.
        try:
            id_registro = int(id_registro)

        except (ValueError, TypeError):
            return None

        # Recorremos los registros.
        for objeto in self.listar():

            if objeto.id == id_registro:
                return objeto

        # None significa que no lo encontramos.
        return None

    # ==============================================
    # BUSCAR REGISTROS POR TEXTO
    # ==============================================

    def buscar(self, texto):

        # Convertimos el texto a minusculas.
        texto = str(texto).strip().lower()

        resultados = []

        # Recorremos los objetos guardados.
        for objeto in self.listar():

            # Revisamos sus campos buscables.
            for campo in self.CAMPOS_BUSCABLES:

                # getattr obtiene un atributo por nombre.
                valor = getattr(objeto, campo, "")

                # Comprobamos si contiene el texto.
                if texto in str(valor).lower():

                    resultados.append(objeto)

                    # Evitamos agregarlo dos veces.
                    break

        return resultados

    # ==============================================
    # ACTUALIZAR UN REGISTRO
    # ==============================================

    def actualizar(self, id_registro, cambios):

        # Primero buscamos el registro.
        actual = self.obtener(id_registro)

        if actual is None:
            raise ValueError("El registro no existe")

        # Convertimos el objeto en diccionario.
        datos = actual.a_diccionario()

        # Modificamos solamente los campos permitidos.
        for campo, valor in cambios.items():

            if campo in self.MODELO.CAMPOS:
                datos[campo] = valor

        # Validamos los nuevos datos.
        self.validar(datos, actual.id)

        # Creamos el objeto actualizado.
        actualizado = self.MODELO.desde_diccionario(datos)

        objetos = self.listar()

        # Buscamos su posicion dentro de la lista.
        for indice, objeto in enumerate(objetos):

            if objeto.id == actual.id:

                # Reemplazamos el objeto anterior.
                objetos[indice] = actualizado
                break

        # Guardamos los cambios.
        self.guardar(objetos)

        return actualizado

    # ==============================================
    # ELIMINAR UN REGISTRO
    # ==============================================

    def eliminar(self, id_registro):

        # Comprobamos que exista.
        actual = self.obtener(id_registro)

        if actual is None:
            raise ValueError("El registro no existe")

        # Creamos una lista sin el registro eliminado.
        restantes = []

        for objeto in self.listar():

            if objeto.id != actual.id:
                restantes.append(objeto)

        # Guardamos la nueva lista.
        self.guardar(restantes)

        return True


# ==================================================
# CLASE 2: MENU CRUD
# ==================================================

# Esta clase muestra las opciones en pantalla.
# Tambien pide los datos utilizando input().
#
# El mismo menu funcionara con estudiantes,
# docentes y materias gracias al polimorfismo.

class MenuCRUD:

    # ==============================================
    # CONSTRUCTOR DEL MENU
    # ==============================================

    def __init__(self, controlador):

        # Guardamos el controlador recibido.
        self._controlador = controlador

    # ==============================================
    # MOSTRAR UNA LISTA DE OBJETOS
    # ==============================================

    def mostrar_registros(self, objetos):

        if not objetos:
            imprimir_info("No hay registros para mostrar")
            return

        for objeto in objetos:
            print(objeto)

    # ==============================================
    # PEDIR DATOS AL USUARIO
    # ==============================================

    def pedir_datos(self, actuales=None):

        # Aqui guardaremos los datos ingresados.
        datos = {}

        # Obtenemos los campos del modelo.
        campos = self._controlador.MODELO.CAMPOS

        # Recorremos cada campo.
        for campo in campos:

            # Comprobamos si el campo es obligatorio.
            obligatorio = (
                campo in self._controlador.MODELO.OBLIGATORIOS
            )

            # Si estamos creando un registro:
            if actuales is None:

                valor = input(f"{campo}: ").strip()

                # Comprobamos los campos obligatorios.
                if not valor and obligatorio:
                    raise ValueError(
                        f"El campo {campo} es obligatorio"
                    )

                # Guardamos el valor recibido.
                # Los campos opcionales vacios tambien
                # pueden llegar al constructor del modelo.
                datos[campo] = valor

            # Si estamos actualizando un registro:
            else:

                anterior = getattr(actuales, campo, "")

                if anterior is None:
                    anterior = ""

                valor = input(
                    f"{campo} [{anterior}]: "
                ).strip()

                # ENTER conserva el valor anterior.
                if valor:
                    datos[campo] = valor

        return datos

    # ==============================================
    # CREAR
    # ==============================================

    def crear(self):

        imprimir_titulo(
            f"REGISTRAR {self._controlador.NOMBRE.upper()}"
        )

        try:

            # Pedimos los datos al usuario.
            datos = self.pedir_datos()

            # El controlador crea y guarda el objeto.
            nuevo = self._controlador.crear(datos)

            imprimir_exito("Registro creado correctamente")

            print(nuevo)

        except (ValueError, TypeError) as error:

            imprimir_error(str(error))

    # ==============================================
    # LISTAR
    # ==============================================

    def listar(self):

        imprimir_titulo(
            f"LISTADO DE {self._controlador.NOMBRE.upper()}"
        )

        objetos = self._controlador.listar()

        self.mostrar_registros(objetos)

    # ==============================================
    # BUSCAR
    # ==============================================

    def buscar(self):

        imprimir_titulo("BUSCAR REGISTRO")

        texto = input("Escribe el texto que buscas: ").strip()

        resultados = self._controlador.buscar(texto)

        self.mostrar_registros(resultados)

    # ==============================================
    # CONSULTAR POR ID
    # ==============================================

    def ver_por_id(self):

        imprimir_titulo("CONSULTAR POR ID")

        id_registro = input("Escribe el ID: ").strip()

        objeto = self._controlador.obtener(id_registro)

        if objeto is None:
            imprimir_error("Registro no encontrado")
            return

        print(objeto)

    # ==============================================
    # ACTUALIZAR
    # ==============================================

    def actualizar(self):

        imprimir_titulo("ACTUALIZAR REGISTRO")

        id_registro = input("ID que deseas actualizar: ").strip()

        actual = self._controlador.obtener(id_registro)

        if actual is None:
            imprimir_error("Registro no encontrado")
            return

        print("\nDatos actuales:")
        print(actual)

        print("\nPresiona ENTER para conservar un dato.")

        try:

            cambios = self.pedir_datos(actual)

            actualizado = self._controlador.actualizar(
                id_registro,
                cambios
            )

            imprimir_exito("Registro actualizado correctamente")

            print(actualizado)

        except (ValueError, TypeError) as error:

            imprimir_error(str(error))

    # ==============================================
    # ELIMINAR
    # ==============================================

    def eliminar(self):

        imprimir_titulo("ELIMINAR REGISTRO")

        id_registro = input("ID que deseas eliminar: ").strip()

        objeto = self._controlador.obtener(id_registro)

        if objeto is None:
            imprimir_error("Registro no encontrado")
            return

        print(objeto)

        # Pedimos confirmacion antes de borrar.
        if not confirmar("¿Seguro que deseas eliminarlo? (s/n): "):

            imprimir_info("Operacion cancelada")
            return

        try:

            self._controlador.eliminar(id_registro)

            imprimir_exito("Registro eliminado correctamente")

        except (ValueError, TypeError) as error:

            imprimir_error(str(error))

    # ==============================================
    # MOSTRAR LAS OPCIONES
    # ==============================================

    def mostrar_opciones(self):

        imprimir_titulo(
            f"MENU DE {self._controlador.NOMBRE.upper()}"
        )

        print("1. Registrar")
        print("2. Listar")
        print("3. Buscar")
        print("4. Consultar por ID")
        print("5. Actualizar")
        print("6. Eliminar")
        print("0. Volver al menu principal")

    # ==============================================
    # EJECUTAR EL MENU
    # ==============================================

    def ejecutar(self):

        # El ciclo mantiene abierto este menu.
        while True:

            self.mostrar_opciones()

            opcion = input("\nElige una opcion: ").strip()

            if opcion == "1":
                self.crear()

            elif opcion == "2":
                self.listar()

            elif opcion == "3":
                self.buscar()

            elif opcion == "4":
                self.ver_por_id()

            elif opcion == "5":
                self.actualizar()

            elif opcion == "6":
                self.eliminar()

            elif opcion == "0":
                break

            else:
                imprimir_error("Opcion incorrecta")
