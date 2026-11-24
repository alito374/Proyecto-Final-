
import ply.yacc as yacc
from lexer import tokens, lexer


# Guardar los errores encontrados
errores = []


# Prioridad de las operaciones matemáticas
precedence = (
    ("left", "MAS", "MENOS"),
    ("left", "MULTIPLICACION", "DIVISION"),
)


# Estructura principal de ALMA
def p_programa(p):
    "programa : DESPIERTA instrucciones DESCANSA"
    p[0] = ("programa", p[2])


# Una o varias instrucciones
def p_instrucciones_varias(p):
    "instrucciones : instrucciones instruccion"
    p[0] = p[1] + [p[2]]


def p_instrucciones_una(p):
    "instrucciones : instruccion"
    p[0] = [p[1]]


# Crear o asignar una variable
def p_instruccion_atesora(p):
    "instruccion : ATESORA IDENTIFICADOR IGUAL expresion"
    p[0] = ("atesora", p[2], p[4])


# Mostrar información
def p_instruccion_cuentame(p):
    "instruccion : CUENTAME expresion"
    p[0] = ("cuentame", p[2])


# Operaciones matemáticas
def p_expresion_operacion(p):
    """expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion"""
    p[0] = ("operacion", p[2], p[1], p[3])


# Números, textos y variables
def p_expresion_numero(p):
    "expresion : NUMERO"
    p[0] = ("numero", p[1])


def p_expresion_texto(p):
    "expresion : TEXTO"
    p[0] = ("texto", p[1])


def p_expresion_variable(p):
    "expresion : IDENTIFICADOR"
    p[0] = ("variable", p[1])


# Expresiones entre paréntesis
def p_expresion_parentesis(p):
    "expresion : PARENTESIS_ABRE expresion PARENTESIS_CIERRA"
    p[0] = p[2]


# Detectar errores sintácticos
def p_error(p):
    if p:
        mensaje = (
            f"Error sintáctico en la línea {p.lineno}: "
            f"se encontró '{p.value}'"
        )
    else:
        mensaje = "Error sintáctico: el programa está incompleto."

    errores.append(mensaje)


# Construir el analizador sintáctico
parser = yacc.yacc(write_tables=False, debug=False)


# Analizar un programa ALMA
def analizar(codigo):
    errores.clear()
    lexer.lineno = 1

    resultado = parser.parse(codigo, lexer=lexer)

    if errores:
        return False, errores.copy()

    if resultado is None:
        return False, ["No se pudo analizar el programa."]

    return True, resultado



# Prueba del analizador
if __name__ == "__main__":
    codigo = """DESPIERTA
ATESORA edad = 20
CUENTAME edad
DESCANSA"""

    valido, resultado = analizar(codigo)

    if valido:
        print("Programa ALMA válido.")
        print(resultado)
    else:
        print("Se encontraron errores:")
        for error in resultado:
            print(error)
