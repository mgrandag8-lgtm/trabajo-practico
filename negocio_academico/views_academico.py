
# ==================================================
# SISTEMA ACADEMICO
# Archivo: views_academico.py
# ==================================================

# Importamos nuestros modelos academicos.
from models_academico import (
    Estudiante,
    Docente,
    Materia,
    Matricula
)

# Reutilizamos el CRUD y el menu general.
from views import CrudBase, MenuCRUD

# Funciones para mostrar mensajes.
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info
)


# ==================================================
# 1. CONTROLADOR DE ESTUDIANTES
# ==================================================

# Heredamos las operaciones de CrudBase.
class EstudianteController(CrudBase):

    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    NOMBRE = "estudiante"

    CAMPOS_BUSCABLES = (
        "nombre", "apellido", "email", "carnet"
    )

    # Comprueba que los datos sean correctos.
    def validar(self, datos, id_actual=None):

        # Revisamos los campos obligatorios.
        for campo in self.MODELO.OBLIGATORIOS:

            if not str(datos.get(campo, "")).strip():
                raise ValueError(
                    f"El campo {campo} es obligatorio"
                )

        email = str(datos["email"]).strip().lower()
        carnet = str(datos["carnet"]).strip().upper()

        # Comprobamos que el carnet no este repetido.
        if len(carnet) < 4:
            raise ValueError(
                "El carnet necesita 4 caracteres como minimo"
            )

        # Revisamos los estudiantes registrados.
        for estudiante in self.listar():

            # Si estamos actualizando, ignoramos
            # el registro que estamos modificando.
            if estudiante.id == id_actual:
                continue

            if estudiante.carnet == carnet:
                raise ValueError(
                    "Este carnet ya esta registrado"
                )

            if estudiante.email == email:
                raise ValueError(
                    "Este correo ya esta registrado"
                )

    # No eliminamos estudiantes matriculados.
    def eliminar(self, id_registro):

        estudiante = self.obtener(id_registro)

        if estudiante is None:
            raise ValueError("El estudiante no existe")

        matriculas = MatriculaController().listar()

        for matricula in matriculas:

            if matricula.estudiante_id == estudiante.id:
                raise ValueError(
                    "No puedes eliminar un estudiante "
                    "que tiene matriculas"
                )

        # super() utiliza el metodo del padre.
        return super().eliminar(id_registro)


# ==================================================
# 2. CONTROLADOR DE DOCENTES
# ==================================================

class DocenteController(CrudBase):

    MODELO = Docente
    ARCHIVO = "data/docentes.json"
    NOMBRE = "docente"

    CAMPOS_BUSCABLES = (
        "nombre", "apellido", "email", "especialidad"
    )

    def validar(self, datos, id_actual=None):

        for campo in self.MODELO.OBLIGATORIOS:

            if not str(datos.get(campo, "")).strip():
                raise ValueError(
                    f"El campo {campo} es obligatorio"
                )

        email = str(datos["email"]).strip().lower()

        # No permitimos dos docentes con el mismo email.
        for docente in self.listar():

            if docente.id == id_actual:
                continue

            if docente.email == email:
                raise ValueError(
                    "Ya existe un docente con ese correo"
                )

    # Protegemos los docentes asignados.
    def eliminar(self, id_registro):

        docente = self.obtener(id_registro)

        if docente is None:
            raise ValueError("El docente no existe")

        materias = MateriaController(self).listar()

        for materia in materias:

            if materia.docente_id == docente.id:
                raise ValueError(
                    "No puedes eliminar un docente "
                    "asignado a una materia"
                )

        return super().eliminar(id_registro)


# ==================================================
# 3. CONTROLADOR DE MATERIAS
# ==================================================

class MateriaController(CrudBase):

    MODELO = Materia
    ARCHIVO = "data/materias.json"
    NOMBRE = "materia"

    CAMPOS_BUSCABLES = ("nombre", "codigo")

    # Recibimos el controlador de docentes.
    def __init__(self, docentes=None):

        super().__init__()

        if docentes is None:
            docentes = DocenteController()

        self.docentes = docentes

    # Validamos materias y docentes.
    def validar(self, datos, id_actual=None):

        for campo in self.MODELO.OBLIGATORIOS:

            if not str(datos.get(campo, "")).strip():
                raise ValueError(
                    f"El campo {campo} es obligatorio"
                )

        codigo = str(datos["codigo"]).strip().upper()

        if len(codigo) < 3:
            raise ValueError(
                "El codigo necesita minimo 3 caracteres"
            )

        # No permitimos codigos repetidos.
        for materia in self.listar():

            if materia.id == id_actual:
                continue

            if materia.codigo == codigo:
                raise ValueError(
                    "Ya existe una materia con ese codigo"
                )

        # Validamos la cantidad de creditos.
        try:
            creditos = int(datos.get("creditos") or 0)

        except (ValueError, TypeError):
            raise ValueError(
                "Los creditos deben ser un numero entero"
            )

        if creditos < 0 or creditos > 10:
            raise ValueError(
                "Los creditos deben estar entre 0 y 10"
            )

        # Una materia puede no tener docente.
        docente_id = datos.get("docente_id")

        if docente_id is not None and str(docente_id).strip() not in ("", "0"):

            docente = self.docentes.obtener(docente_id)

            if docente is None:
                raise ValueError(
                    "El docente asignado no existe"
                )

    # Permite cambiar el docente de una materia.
    def asignar_docente(self, materia_id, docente_id):

        if self.obtener(materia_id) is None:
            raise ValueError("La materia no existe")

        if self.docentes.obtener(docente_id) is None:
            raise ValueError("El docente no existe")

        return self.actualizar(
            materia_id,
            {"docente_id": docente_id}
        )

    # Devuelve las materias de un docente.
    def materias_de_docente(self, docente_id):

        docente = self.docentes.obtener(docente_id)

        if docente is None:
            raise ValueError("El docente no existe")

        resultado = []

        for materia in self.listar():

            if materia.docente_id == docente.id:
                resultado.append(materia)

        return resultado

    # No eliminamos materias con matriculas.
    def eliminar(self, id_registro):

        materia = self.obtener(id_registro)

        if materia is None:
            raise ValueError("La materia no existe")

        for matricula in MatriculaController().listar():

            if matricula.materia_id == materia.id:
                raise ValueError(
                    "No puedes eliminar una materia "
                    "con estudiantes matriculados"
                )

        return super().eliminar(id_registro)


# ==================================================
# 4. CONTROLADOR DE MATRICULAS
# ==================================================

class MatriculaController(CrudBase):

    MODELO = Matricula
    ARCHIVO = "data/matriculas.json"
    NOMBRE = "matricula"

    CAMPOS_BUSCABLES = ("periodo",)

    def __init__(self, estudiantes=None, materias=None):

        super().__init__()

        if estudiantes is None:
            estudiantes = EstudianteController()

        if materias is None:
            materias = MateriaController()

        self.estudiantes = estudiantes
        self.materias = materias

    # ==============================================
    # VALIDAR MATRICULA
    # ==============================================

    def validar(self, datos, id_actual=None):

        estudiante_id = datos.get("estudiante_id")
        materia_id = datos.get("materia_id")

        periodo = str(
            datos.get("periodo") or "2026-1"
        ).strip()

        # El estudiante debe existir.
        estudiante = self.estudiantes.obtener(
            estudiante_id
        )

        if estudiante is None:
            raise ValueError(
                "El estudiante no esta registrado"
            )

        # La materia tambien debe existir.
        materia = self.materias.obtener(materia_id)

        if materia is None:
            raise ValueError(
                "La materia no esta registrada"
            )

        # Evitamos matricular dos veces
        # al mismo estudiante en la misma materia
        # durante el mismo periodo.
        for matricula in self.listar():

            if matricula.id == id_actual:
                continue

            if (
                matricula.estudiante_id == estudiante.id
                and matricula.materia_id == materia.id
                and matricula.periodo == periodo
            ):
                raise ValueError(
                    "El estudiante ya esta matriculado "
                    "en esa materia y periodo"
                )

    # ==============================================
    # ACTUALIZAR SIN BORRAR NOTAS
    # ==============================================

    # Sobrescribimos el metodo general porque
    # las matriculas contienen notas adicionales.
    def actualizar(self, id_registro, cambios):

        actual = self.obtener(id_registro)

        if actual is None:
            raise ValueError("La matricula no existe")

        # Obtenemos todos los datos, incluidas notas.
        datos = actual.a_diccionario()

        # Solo cambiamos los campos autorizados.
        for campo, valor in cambios.items():

            if campo in self.MODELO.CAMPOS:
                datos[campo] = valor

        self.validar(datos, actual.id)

        # Recuperamos tambien las notas anteriores.
        actualizado = Matricula.desde_diccionario(
            datos
        )

        objetos = self.listar()

        for indice, objeto in enumerate(objetos):

            if objeto.id == actual.id:
                objetos[indice] = actualizado
                break

        self.guardar(objetos)

        return actualizado

    # ==============================================
    # AGREGAR NOTA
    # ==============================================

    def agregar_nota(
        self, matricula_id, tipo, valor, peso=1
    ):

        matricula = self.obtener(matricula_id)

        if matricula is None:
            raise ValueError(
                "La matricula no existe"
            )

        # El modelo Nota valida el valor y el tipo.
        nueva_nota = matricula.agregar_nota(
            tipo, valor, peso
        )

        # Buscamos la matricula en la lista.
        objetos = self.listar()

        for indice, objeto in enumerate(objetos):

            if objeto.id == matricula.id:

                objetos[indice] = matricula
                break

        # Es obligatorio guardar despues de agregar.
        self.guardar(objetos)

        return nueva_nota

    # ==============================================
    # GENERAR BOLETIN
    # ==============================================

    def boletin(self, estudiante_id):

        estudiante = self.estudiantes.obtener(
            estudiante_id
        )

        if estudiante is None:
            raise ValueError(
                "El estudiante no existe"
            )

        # Buscamos sus matriculas.
        matriculas = []

        for matricula in self.listar():

            if matricula.estudiante_id == estudiante.id:
                matriculas.append(matricula)

        # Preparamos las lineas del boletin.
        lineas = [
            "=" * 50,
            "BOLETIN ACADEMICO",
            "=" * 50,
            f"Estudiante: {estudiante.nombre_completo}",
            f"Carnet: {estudiante.carnet}",
            "-" * 50
        ]

        if not matriculas:
            lineas.append(
                "El estudiante no tiene matriculas"
            )
            return "\n".join(lineas)

        promedios = []

        for matricula in matriculas:

            materia = self.materias.obtener(
                matricula.materia_id
            )

            if materia is None:
                nombre_materia = "Materia no encontrada"
            else:
                nombre_materia = materia.nombre

            lineas.append(
                f"Materia: {nombre_materia}"
            )

            lineas.append(
                f"Periodo: {matricula.periodo}"
            )

            # Mostramos cada nota registrada.
            if matricula.notas:

                for nota in matricula.notas:

                    lineas.append(
                        f"  {nota.tipo}: {nota.valor} "
                        f"(peso {nota.peso:g})"
                    )

                promedios.append(matricula.promedio)

            else:
                lineas.append("  Sin notas")

            lineas.append(
                f"Promedio: {matricula.promedio:.2f}"
            )

            lineas.append(
                f"Estado: {matricula.estado}"
            )

            lineas.append("-" * 50)

        # Promedio general de materias con notas.
        if promedios:

            promedio_general = (
                sum(promedios) / len(promedios)
            )

            lineas.append(
                f"Promedio general: {promedio_general:.2f}"
            )

        else:
            lineas.append(
                "Promedio general: Sin notas"
            )

        # Convertimos la lista en un texto.
        return "\n".join(lineas)

    # ==============================================
    # ESTUDIANTES REPROBADOS
    # ==============================================

    def estudiantes_reprobados(self):

        resultados = []

        for matricula in self.listar():

            if matricula.estado != "Reprobado":
                continue

            estudiante = self.estudiantes.obtener(
                matricula.estudiante_id
            )

            materia = self.materias.obtener(
                matricula.materia_id
            )

            if estudiante is None or materia is None:
                continue

            resultados.append({
                "estudiante": estudiante.nombre_completo,
                "materia": materia.nombre,
                "promedio": matricula.promedio,
                "periodo": matricula.periodo
            })

        return resultados


# ==================================================
# 5. MENU ESPECIAL DE MATRICULAS
# ==================================================

# Heredamos el menu CRUD para reutilizar
# listar, buscar, actualizar y eliminar.
class MenuMatriculas(MenuCRUD):

    # ==============================================
    # REGISTRAR MATRICULA
    # ==============================================

    def crear(self):

        imprimir_titulo("REGISTRAR MATRICULA")

        print("\nESTUDIANTES:")
        self.mostrar_registros(
            self._controlador.estudiantes.listar()
        )

        print("\nMATERIAS:")
        self.mostrar_registros(
            self._controlador.materias.listar()
        )

        try:
            estudiante_id = input(
                "\nID del estudiante: "
            ).strip()

            materia_id = input(
                "ID de la materia: "
            ).strip()

            periodo = input(
                "Periodo [2026-1]: "
            ).strip()

            datos = {
                "estudiante_id": estudiante_id,
                "materia_id": materia_id,
                "periodo": periodo or "2026-1"
            }

            nueva = self._controlador.crear(datos)

            imprimir_exito(
                "Matricula registrada correctamente"
            )

            print(nueva)

        except (ValueError, TypeError) as error:
            imprimir_error(str(error))

    # ==============================================
    # AGREGAR NOTA
    # ==============================================

    def agregar_nota(self):

        imprimir_titulo("AGREGAR NOTA")

        self.mostrar_registros(
            self._controlador.listar()
        )

        try:
            matricula_id = input(
                "\nID de la matricula: "
            ).strip()

            print("\nTIPOS DE NOTA")
            print("1. Deber")
            print("2. Leccion")
            print("3. Examen")

            opcion = input(
                "Elige un tipo: "
            ).strip()

            # Relacionamos cada opcion con un tipo.
            tipos = {
                "1": "deber",
                "2": "lección",
                "3": "examen"
            }

            if opcion not in tipos:
                raise ValueError(
                    "Tipo de nota incorrecto"
                )

            valor = input(
                "Calificacion (0 a 20): "
            ).strip()

            peso = input(
                "Peso de la nota [1]: "
            ).strip()

            nota = self._controlador.agregar_nota(
                matricula_id,
                tipos[opcion],
                valor,
                peso or 1
            )

            imprimir_exito(
                "Nota registrada correctamente"
            )

            print(nota)

        except (ValueError, TypeError) as error:
            imprimir_error(str(error))

    # ==============================================
    # MOSTRAR BOLETIN
    # ==============================================

    def ver_boletin(self):

        imprimir_titulo("VER BOLETIN")

        self.mostrar_registros(
            self._controlador.estudiantes.listar()
        )

        estudiante_id = input(
            "\nID del estudiante: "
        ).strip()

        try:
            resultado = self._controlador.boletin(
                estudiante_id
            )

            print("\n" + resultado)

        except (ValueError, TypeError) as error:
            imprimir_error(str(error))

    # ==============================================
    # MOSTRAR REPROBADOS
    # ==============================================

    def ver_reprobados(self):

        imprimir_titulo("ESTUDIANTES REPROBADOS")

        resultados = (
            self._controlador.estudiantes_reprobados()
        )

        if not resultados:
            imprimir_info(
                "No hay estudiantes reprobados"
            )
            return

        for registro in resultados:

            print(
                f"\nEstudiante: {registro['estudiante']}"
            )

            print(
                f"Materia: {registro['materia']}"
            )

            print(
                f"Promedio: {registro['promedio']}"
            )

            print(
                f"Periodo: {registro['periodo']}"
            )

    # ==============================================
    # MOSTRAR OPCIONES
    # ==============================================

    def mostrar_opciones(self):

        imprimir_titulo("MENU DE MATRICULAS")

        print("1. Registrar matricula")
        print("2. Listar matriculas")
        print("3. Buscar matriculas")
        print("4. Consultar por ID")
        print("5. Actualizar matricula")
        print("6. Eliminar matricula")
        print("7. Agregar nota")
        print("8. Ver boletin")
        print("9. Estudiantes reprobados")
        print("0. Volver al menu principal")

    # ==============================================
    # EJECUTAR MENU
    # ==============================================

    def ejecutar(self):

        while True:

            self.mostrar_opciones()

            opcion = input(
                "\nElige una opcion: "
            ).strip()

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

            elif opcion == "7":
                self.agregar_nota()

            elif opcion == "8":
                self.ver_boletin()

            elif opcion == "9":
                self.ver_reprobados()

            elif opcion == "0":
                break

            else:
                imprimir_error("Opcion incorrecta")
