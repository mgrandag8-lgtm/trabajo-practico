
# ==================================================
# SISTEMA ACADEMICO
# Archivo: shared/herramientas.py
# ==================================================

# Este archivo contiene funciones que podemos
# utilizar en diferentes partes del programa.


# ==============================================
# MOSTRAR TITULOS
# ==============================================

# Recibe un texto y lo muestra como titulo.
def imprimir_titulo(titulo):

    # Dejamos un espacio antes del titulo.
    print()

    # Mostramos una linea decorativa.
    print("=" * 50)

    # Mostramos el titulo centrado.
    print(titulo.center(50))

    # Mostramos otra linea decorativa.
    print("=" * 50)


# ==============================================
# MOSTRAR MENSAJES DE EXITO
# ==============================================

# Se utiliza cuando una operacion sale bien.
def imprimir_exito(mensaje):

    print("✓", mensaje)


# ==============================================
# MOSTRAR MENSAJES DE ERROR
# ==============================================

# Se utiliza cuando ocurre un problema.
def imprimir_error(mensaje):

    print("✗", mensaje)


# ==============================================
# MOSTRAR INFORMACION
# ==============================================

# Se utiliza para mostrar informacion al usuario.
def imprimir_info(mensaje):

    print("•", mensaje)


# ==============================================
# CONFIRMAR UNA ACCION
# ==============================================

# Pregunta si el usuario desea continuar.
def confirmar(texto="¿Confirmar? (s/n): "):

    # Pedimos una respuesta al usuario.
    respuesta = input(texto)

    # Quitamos espacios y convertimos a minusculas.
    respuesta = respuesta.strip().lower()

    # Devolvemos True si responde afirmativamente.
    # En cualquier otro caso devolvemos False.
    return respuesta in ("s", "si", "sí")
