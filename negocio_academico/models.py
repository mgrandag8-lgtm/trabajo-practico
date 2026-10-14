
# ==================================================
# SISTEMA ACADEMICO
# Archivo: models.py
# ==================================================

# ABC permite crear clases abstractas.
# abstractmethod permite crear metodos obligatorios.
from abc import ABC, abstractmethod


# ==================================================
# CLASE 1: MODELO BASE
# ==================================================

# Esta es la clase principal de nuestros modelos.
# Las otras clases podran heredar sus funciones.

class ModeloBase(ABC):

    # CAMPOS indica los datos que tiene un modelo.
    # Las clases hijas definiran sus propios campos.
    CAMPOS = ()

    # OBLIGATORIOS indica los datos que no pueden faltar.
    OBLIGATORIOS = ()

    # __init__ se ejecuta al crear un objeto.
    def __init__(self, id_registro):

        # Convertimos el ID a un numero entero.
        id_registro = int(id_registro)

        # Un ID debe ser mayor que cero.
        if id_registro <= 0:
            raise ValueError("El ID debe ser positivo")

        # Guardamos el ID como atributo privado.
        self.__id = id_registro

    # ==============================================
    # CONSULTAR EL ID
    # ==============================================

    # property permite consultar un atributo privado.
    @property
    def id(self):

        return self.__id

    # ==============================================
    # LIMPIAR TEXTOS
    # ==============================================

    # staticmethod permite utilizar esta funcion
    # sin necesitar los datos de un objeto.

    @staticmethod
    def limpiar(texto):

        # str convierte el dato en texto.
        # strip elimina espacios al inicio y al final.
        return str(texto).strip()

    # ==============================================
    # CONVERTIR A DICCIONARIO
    # ==============================================

    # Las clases hijas deben crear este metodo.
    # Se utilizara para guardar los objetos en JSON.

    @abstractmethod
    def a_diccionario(self):
        pass

    # ==============================================
    # MOSTRAR INFORMACION DEL OBJETO
    # ==============================================

    # Cada clase hija mostrara sus datos
    # de una forma diferente.

    @abstractmethod
    def etiqueta(self):
        pass

    # ==============================================
    # CREAR OBJETO DESDE UN DICCIONARIO
    # ==============================================

    # classmethod permite trabajar con la clase.
    # cls representa la clase que lo esta utilizando.

    @classmethod
    def desde_diccionario(cls, datos):

        # Creamos un diccionario con los campos.
        valores = {}

        # Recorremos los campos de la clase.
        for campo in cls.CAMPOS:

            # Obtenemos el valor guardado.
            valores[campo] = datos.get(campo, "")

        # Creamos el objeto con sus datos.
        return cls(datos["id"], **valores)

    # ==============================================
    # CONVERTIR OBJETO EN TEXTO
    # ==============================================

    # Este metodo se utiliza cuando hacemos print(objeto).
    def __str__(self):

        # Mostramos el ID y la etiqueta del objeto.
        return f"[{self.id}] {self.etiqueta()}"


# ==================================================
# CLASE 2: PERSONA
# ==================================================

# Persona hereda de ModeloBase.
# Estudiante y Docente heredaran de Persona.

class Persona(ModeloBase):

    # Los datos que tendra una persona.
    CAMPOS = ("nombre", "apellido", "email")

    # Estos datos son obligatorios.
    OBLIGATORIOS = ("nombre", "apellido", "email")

    # ==============================================
    # CONSTRUCTOR DE PERSONA
    # ==============================================

    def __init__(self, id_registro, nombre, apellido, email):

        # super llama al constructor de ModeloBase.
        # Asi reutilizamos la validacion del ID.
        super().__init__(id_registro)

        # Guardamos los datos usando sus propiedades.
        # Los setters comprobaran que sean validos.
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    # ==============================================
    # VALIDAR CORREO ELECTRONICO
    # ==============================================

    @staticmethod
    def es_email_valido(texto):

        texto = str(texto).strip()

        # El correo debe contener exactamente una @.
        if texto.count("@") != 1:
            return False

        # Separamos el usuario y el dominio.
        usuario, dominio = texto.split("@")

        # Comprobamos algunas reglas basicas.
        if not usuario:
            return False

        if "." not in dominio:
            return False

        if dominio.startswith(".") or dominio.endswith("."):
            return False

        return True

    # ==============================================
    # NOMBRE
    # ==============================================

    # Permite consultar el nombre.
    @property
    def nombre(self):
        return self.__nombre

    # Permite modificar el nombre con validacion.
    @nombre.setter
    def nombre(self, valor):

        valor = self.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        # title pone mayuscula al inicio de cada palabra.
        self.__nombre = valor.title()

    # ==============================================
    # APELLIDO
    # ==============================================

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):

        valor = self.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    # ==============================================
    # CORREO ELECTRONICO
    # ==============================================

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):

        valor = self.limpiar(valor)

        if not self.es_email_valido(valor):
            raise ValueError("Correo electronico invalido")

        # Guardamos el correo en minusculas.
        self.__email = valor.lower()

    # ==============================================
    # NOMBRE COMPLETO
    # ==============================================

    # Esta propiedad une el nombre y apellido.
    @property
    def nombre_completo(self):

        return f"{self.nombre} {self.apellido}"

    # ==============================================
    # CONVERTIR PERSONA A DICCIONARIO
    # ==============================================

    # Este metodo sera reutilizado por
    # Estudiante y Docente usando super().

    def a_diccionario(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }
