
# ==================================================
# SISTEMA ACADEMICO
# Archivo principal: main.py
# ==================================================

# Importamos los menus y controladores que usaremos.

from views import MenuCRUD

from views_academico import (
    EstudianteController,
    DocenteController,
    MateriaController,
    MatriculaController,
    MenuMatriculas
)


# Esta clase organiza el menu principal.
class MenuPrincipal:

    # __init__ se ejecuta al crear el menu.
    def __init__(self):

        # Creamos los controladores.
        # Cada uno se encarga de una parte del sistema.

        self.estudiantes = EstudianteController()
        self.docentes = DocenteController()

        # Las materias necesitan consultar los docentes.
        self.materias = MateriaController(self.docentes)

        # Las matriculas necesitan estudiantes y materias.
        self.matriculas = MatriculaController(
            self.estudiantes,
            self.materias
        )

        # Creamos los menus para cada entidad.
        self.menu_estudiantes = MenuCRUD(self.estudiantes)
        self.menu_docentes = MenuCRUD(self.docentes)
        self.menu_materias = MenuCRUD(self.materias)
        self.menu_matriculas = MenuMatriculas(self.matriculas)

    # Esta funcion muestra las opciones.
    def mostrar_menu(self):

        print("\n====================================")
        print("       SISTEMA ACADEMICO")
        print("====================================")
        print("1. Estudiantes")
        print("2. Docentes")
        print("3. Materias")
        print("4. Matriculas y notas")
        print("0. Salir")

    # Esta funcion hace funcionar el menu.
    def ejecutar(self):

        # El ciclo mantiene el programa abierto.
        while True:

            self.mostrar_menu()

            # El usuario escribe una opcion.
            opcion = input("\nElige una opcion: ")

            # Segun la opcion, abrimos un menu.
            if opcion == "1":
                self.menu_estudiantes.ejecutar()

            elif opcion == "2":
                self.menu_docentes.ejecutar()

            elif opcion == "3":
                self.menu_materias.ejecutar()

            elif opcion == "4":
                self.menu_matriculas.ejecutar()

            elif opcion == "0":
                print("Gracias por usar el sistema.")
                break

            else:
                print("Opcion incorrecta. Intenta otra vez.")


# Esta condicion inicia el programa.
if __name__ == "__main__":

    # Creamos el objeto del menu principal.
    programa = MenuPrincipal()

    # Ejecutamos el programa.
    programa.ejecutar()
