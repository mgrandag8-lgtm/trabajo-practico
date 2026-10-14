
# ==================================================
# SISTEMA ACADEMICO
# Archivo: models_academico.py
# ==================================================

# Importamos las clases base que ya programamos.
from models import ModeloBase, Persona


# ==================================================
# CLASE 1: ESTUDIANTE
# ==================================================

# Estudiante hereda de Persona.
# Ya tiene nombre, apellido y email.
# Solo necesitamos agregar el carnet.

class Estudiante(Persona):

    CAMPOS = Persona.CAMPOS + ("carnet",)

    OBLIGATORIOS = Persona.OBLIGATORIOS + ("carnet",)

    # Constructor del estudiante.
    def __init__(self, id_registro, nombre, apellido, email, carnet):

        # Reutilizamos el constructor de Persona.
        super().__init__(id_registro, nombre, apellido, email)

        # Guardamos el carnet usando su validacion.
        self.carnet = carnet

    # Permite consultar el carnet.
    @property
    def carnet(self):
        return self.__carnet

    # Permite modificar y validar el carnet.
    @carnet.setter
    def carnet(self, valor):

        valor = self.limpiar(valor).upper()

        if len(valor) < 4:
            raise ValueError(
                "El carnet debe tener al menos 4 caracteres"
            )

        self.__carnet = valor

    # Convierte el estudiante en un diccionario.
    # Esto permite guardarlo en JSON.
    def a_diccionario(self):

        datos = super().a_diccionario()

        datos["carnet"] = self.carnet

        return datos

    # Devuelve el texto que veremos al listar.
    def etiqueta(self):

        return f"{self.nombre_completo} - Carnet: {self.carnet}"


# ==================================================
# CLASE 2: DOCENTE
# ==================================================

# Docente tambien hereda de Persona.
# Agregamos titulo y especialidad.

class Docente(Persona):

    CAMPOS = Persona.CAMPOS + ("titulo", "especialidad")

    OBLIGATORIOS = Persona.OBLIGATORIOS

    def __init__(
        self, id_registro, nombre, apellido,
        email, titulo="", especialidad=""
    ):

        super().__init__(id_registro, nombre, apellido, email)

        self.titulo = titulo
        self.especialidad = especialidad

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):

        self.__titulo = self.limpiar(valor)

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, valor):

        self.__especialidad = self.limpiar(valor).title()

    # Preparamos los datos para JSON.
    def a_diccionario(self):

        datos = super().a_diccionario()

        datos["titulo"] = self.titulo
        datos["especialidad"] = self.especialidad

        return datos

    def etiqueta(self):

        return (
            f"{self.nombre_completo} - "
            f"Especialidad: {self.especialidad or 'Sin especialidad'}"
        )


# ==================================================
# CLASE 3: MATERIA
# ==================================================

# Una materia existe independientemente.
# Puede tener un docente asignado.

class Materia(ModeloBase):

    CAMPOS = ("nombre", "codigo", "creditos", "docente_id")

    OBLIGATORIOS = ("nombre", "codigo")

    def __init__(
        self, id_registro, nombre, codigo,
        creditos=0, docente_id=None
    ):

        super().__init__(id_registro)

        self.nombre = nombre
        self.codigo = codigo
        self.creditos = creditos
        self.docente_id = docente_id

    # ==============================================
    # NOMBRE DE LA MATERIA
    # ==============================================

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        valor = self.limpiar(valor)

        if not valor:
            raise ValueError("La materia necesita un nombre")

        self.__nombre = valor.title()

    # ==============================================
    # CODIGO DE LA MATERIA
    # ==============================================

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):

        valor = self.limpiar(valor).upper()

        if len(valor) < 3:
            raise ValueError(
                "El codigo debe tener al menos 3 caracteres"
            )

        self.__codigo = valor

    # ==============================================
    # CREDITOS
    # ==============================================

    @property
    def creditos(self):
        return self.__creditos

    @creditos.setter
    def creditos(self, valor):

        try:
            numero = int(valor or 0)

        except (ValueError, TypeError):
            raise ValueError("Los creditos deben ser un numero")

        if numero < 0 or numero > 10:
            raise ValueError(
                "Los creditos deben estar entre 0 y 10"
            )

        self.__creditos = numero

    # ==============================================
    # DOCENTE ASIGNADO
    # ==============================================

    @property
    def docente_id(self):
        return self.__docente_id

    @docente_id.setter
    def docente_id(self, valor):

        # Una materia puede estar sin docente.
        if valor is None or str(valor).strip() in ("", "0"):

            self.__docente_id = None
            return

        try:
            numero = int(valor)

        except (ValueError, TypeError):
            raise ValueError("El ID del docente debe ser un numero")

        if numero <= 0:
            raise ValueError("El ID del docente debe ser positivo")

        self.__docente_id = numero

    # Convertimos la materia en diccionario.
    def a_diccionario(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "creditos": self.creditos,
            "docente_id": self.docente_id
        }

    # Mostramos la informacion de la materia.
    def etiqueta(self):

        return (
            f"{self.codigo} - {self.nombre} - "
            f"Creditos: {self.creditos} - "
            f"Docente ID: {self.docente_id or 'Sin asignar'}"
        )


# ==================================================
# CLASE 4: NOTA
# ==================================================

# Esta clase representa una calificacion.
# Una nota pertenece a una matricula.

class Nota:

    # Tipos de evaluacion permitidos.
    TIPOS = ("deber", "lección", "examen")

    def __init__(self, tipo, valor, peso=1):

        self.tipo = tipo
        self.valor = valor
        self.peso = peso

    # ==============================================
    # TIPO DE NOTA
    # ==============================================

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):

        valor = str(valor).strip().lower()

        # Aceptamos tambien la palabra sin tilde.
        if valor == "leccion":
            valor = "lección"

        if valor not in self.TIPOS:
            raise ValueError(
                "El tipo debe ser deber, leccion o examen"
            )

        self.__tipo = valor

    # ==============================================
    # VALOR DE LA NOTA
    # ==============================================

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, numero):

        try:
            numero = float(numero)

        except (ValueError, TypeError):
            raise ValueError("La nota debe ser un numero")

        # La nota debe estar entre 0 y 20.
        if not 0 <= numero <= 20:
            raise ValueError("La nota debe estar entre 0 y 20")

        self.__valor = round(numero, 2)

    # ==============================================
    # PESO DE LA NOTA
    # ==============================================

    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, numero):

        try:
            numero = float(numero)

        except (ValueError, TypeError):
            raise ValueError("El peso debe ser un numero")

        if numero <= 0 or numero == float("inf"):
            raise ValueError("El peso debe ser positivo y finito")

        self.__peso = numero

    # Guardamos la nota como diccionario.
    def a_diccionario(self):

        return {
            "tipo": self.tipo,
            "valor": self.valor,
            "peso": self.peso
        }

    # Recuperamos una nota desde JSON.
    @classmethod
    def desde_diccionario(cls, datos):

        return cls(
            datos["tipo"],
            datos["valor"],
            datos.get("peso", 1)
        )

    # Texto que representa la nota.
    def __str__(self):

        return f"{self.tipo}: {self.valor} (peso {self.peso:g})"


# ==================================================
# CLASE 5: MATRICULA
# ==================================================

# Una matricula relaciona estudiante y materia.
# Dentro de ella guardamos las notas.

class Matricula(ModeloBase):

    # Estos son los datos que pediremos en el menu.
    # Las notas se agregan por separado.
    CAMPOS = ("estudiante_id", "materia_id", "periodo")

    OBLIGATORIOS = ("estudiante_id", "materia_id")

    # Puedes cambiar esta nota para modificar
    # la calificacion minima de aprobacion.
    NOTA_APROBACION = 14

    def __init__(
        self, id_registro, estudiante_id,
        materia_id, periodo="", notas=None
    ):

        super().__init__(id_registro)

        self.estudiante_id = estudiante_id
        self.materia_id = materia_id
        self.periodo = periodo

        # Esta lista privada guarda las notas.
        self.__notas = []

        # Recuperamos notas cuando leemos un JSON.
        if notas is not None:

            for nota in notas:

                if not isinstance(nota, Nota):
                    raise ValueError(
                        "Solo se pueden agregar objetos Nota"
                    )

                self.__notas.append(nota)

    # ==============================================
    # ID DEL ESTUDIANTE
    # ==============================================

    @property
    def estudiante_id(self):
        return self.__estudiante_id

    @estudiante_id.setter
    def estudiante_id(self, valor):

        try:
            numero = int(valor)

        except (ValueError, TypeError):
            raise ValueError("ID de estudiante invalido")

        if numero <= 0:
            raise ValueError("El ID debe ser positivo")

        self.__estudiante_id = numero

    # ==============================================
    # ID DE LA MATERIA
    # ==============================================

    @property
    def materia_id(self):
        return self.__materia_id

    @materia_id.setter
    def materia_id(self, valor):

        try:
            numero = int(valor)

        except (ValueError, TypeError):
            raise ValueError("ID de materia invalido")

        if numero <= 0:
            raise ValueError("El ID debe ser positivo")

        self.__materia_id = numero

    # ==============================================
    # PERIODO ACADEMICO
    # ==============================================

    @property
    def periodo(self):
        return self.__periodo

    @periodo.setter
    def periodo(self, valor):

        # Si el usuario no escribe periodo,
        # utilizamos 2026-1 por defecto.
        self.__periodo = self.limpiar(valor) or "2026-1"

    # ==============================================
    # CONSULTAR NOTAS
    # ==============================================

    @property
    def notas(self):

        # Devolvemos una tupla para proteger
        # la lista interna de notas.
        return tuple(self.__notas)

    # ==============================================
    # AGREGAR NOTA
    # ==============================================

    def agregar_nota(self, tipo, valor, peso=1):

        # Creamos una nota con sus validaciones.
        nueva_nota = Nota(tipo, valor, peso)

        # La agregamos a la matricula.
        self.__notas.append(nueva_nota)

        return nueva_nota

    # ==============================================
    # CALCULAR PROMEDIO
    # ==============================================

    @property
    def promedio(self):

        # Sin notas, el promedio mostrado sera 0.
        if not self.__notas:
            return 0

        suma = 0
        total_pesos = 0

        # Recorremos todas las notas.
        for nota in self.__notas:

            suma += nota.valor * nota.peso

            total_pesos += nota.peso

        # Calculamos el promedio ponderado.
        return round(suma / total_pesos, 2)

    # ==============================================
    # ESTADO ACADEMICO
    # ==============================================

    @property
    def estado(self):

        # Si no hay notas, aun no hay calificacion.
        if not self.__notas:
            return "Sin notas"

        # Comprobamos la nota minima de aprobacion.
        if self.promedio >= self.NOTA_APROBACION:
            return "Aprobado"

        return "Reprobado"

    # ==============================================
    # CONVERTIR MATRICULA EN DICCIONARIO
    # ==============================================

    def a_diccionario(self):

        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "materia_id": self.materia_id,
            "periodo": self.periodo,
            "promedio": self.promedio,
            "estado": self.estado,
            "notas": [
                nota.a_diccionario()
                for nota in self.__notas
            ]
        }

    # ==============================================
    # RECUPERAR MATRICULA DESDE JSON
    # ==============================================

    @classmethod
    def desde_diccionario(cls, datos):

        # Convertimos los diccionarios en objetos Nota.
        notas = []

        for dato_nota in datos.get("notas", []):

            nota = Nota.desde_diccionario(dato_nota)

            notas.append(nota)

        # Construimos la matricula con sus notas.
        return cls(
            datos["id"],
            datos["estudiante_id"],
            datos["materia_id"],
            datos.get("periodo", ""),
            notas
        )

    # ==============================================
    # MOSTRAR MATRICULA
    # ==============================================

    def etiqueta(self):

        return (
            f"Estudiante ID: {self.estudiante_id} - "
            f"Materia ID: {self.materia_id} - "
            f"Periodo: {self.periodo} - "
            f"Promedio: {self.promedio} - "
            f"Estado: {self.estado}"
        )
