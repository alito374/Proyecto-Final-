"""
NOVACODE - ANALIZADOR SINTACTICO
Desarrollado con Python y PLY.
Responsable: Integrante 2 (Berdi)
"""

import ply.yacc as yacc
from lexer import tokens, build_lexer

# ==========================================
# 1. PRECEDENCIA DE OPERADORES
# ==========================================
precedence = (
    ("left", "IGUALIGUAL", "DIFERENTE"),
    ("left", "MENOR", "MENORIGUAL", "MAYOR", "MAYORIGUAL"),
    ("left", "MAS", "MENOS"),
    ("left", "POR", "DIVIDIDO"),
    ("right", "UMINUS"),
)

# Diccionario para guardar variables durante el análisis (Simulador)
variables = {}


# ==========================================
# 2. PROGRAMA PRINCIPAL
# ==========================================
def p_programa(p):
    "programa : INICIO LLAVE_IZQ instrucciones LLAVE_DER FIN"
    p[0] = "Programa NovaCode válido"


# ==========================================
# 3. LISTA DE INSTRUCCIONES
# ==========================================
def p_instrucciones_varias(p):
    "instrucciones : instrucciones instruccion"
    p[0] = None


def p_instrucciones_vacias(p):
    "instrucciones : empty"
    p[0] = None


# ==========================================
# 4. ASIGNACION DE VARIABLES
# ==========================================
def p_instruccion_asignacion(p):
    "instruccion : IDENTIFICADOR IGUAL expresion PUNTO_COMA"
    # Guardamos el valor de la expresión en el diccionario de variables
    variables[p[1]] = p[3]
    p[0] = None


# ==========================================
# 5. INSTRUCCION MOSTRAR
# ==========================================
def p_instruccion_mostrar(p):
    "instruccion : MOSTRAR PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA"
    # Al analizar, imprimimos lo que se va a mostrar (útil para depurar)
    print(f"[MOSTRAR]: {p[3]}")
    p[0] = None


# ==========================================
# 6. CONDICIONAL SI
# ==========================================
def p_instruccion_si(p):
    "instruccion : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque"
    p[0] = None


def p_instruccion_si_sino(p):
    "instruccion : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque SINO bloque"
    p[0] = None


# ==========================================
# 7. CICLO MIENTRAS
# ==========================================
def p_instruccion_mientras(p):
    "instruccion : MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque"
    p[0] = None


# ==========================================
# 8. BLOQUES DE INSTRUCCIONES
# ==========================================
def p_bloque(p):
    "bloque : LLAVE_IZQ instrucciones LLAVE_DER"
    p[0] = None


# ==========================================
# 9. OPERACIONES MATEMATICAS
# ==========================================
def p_expresion_binaria(p):
    """
    expresion : expresion MAS expresion
              | expresion MENOS expresion
              | expresion POR expresion
              | expresion DIVIDIDO expresion
              | expresion IGUALIGUAL expresion
              | expresion DIFERENTE expresion
              | expresion MENOR expresion
              | expresion MENORIGUAL expresion
              | expresion MAYOR expresion
              | expresion MAYORIGUAL expresion
    """
    # Lógica de evaluación de operadores
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            parser.errors.append(f"Error en línea {p.lineno(2)}: División por cero")
            p[0] = 0
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '==':
        p[0] = (p[1] == p[3])
    elif p[2] == '!=':
        p[0] = (p[1] != p[3])
    elif p[2] == '<':
        p[0] = (p[1] < p[3])
    elif p[2] == '<=':
        p[0] = (p[1] <= p[3])
    elif p[2] == '>':
        p[0] = (p[1] > p[3])
    elif p[2] == '>=':
        p[0] = (p[1] >= p[3])


# ==========================================
# 10. NUMEROS NEGATIVOS
# ==========================================
def p_expresion_unaria(p):
    "expresion : MENOS expresion %prec UMINUS"
    p[0] = -p[2]


# ==========================================
# 11. EXPRESIONES ENTRE PARENTESIS
# ==========================================
def p_expresion_parentesis(p):
    "expresion : PARENTESIS_IZQ expresion PARENTESIS_DER"
    p[0] = p[2]


# ==========================================
# 12. VALORES Y VARIABLES
# ==========================================
def p_expresion_atomica(p):
    """
    expresion : NUMERO
              | CADENA
              | IDENTIFICADOR
              | VERDADERO
              | FALSO
    """
    if p.slice[1].type == 'IDENTIFICADOR':
        # Si es una variable, buscamos su valor en el diccionario
        p[0] = variables.get(p[1], 0)  # Si no existe, asume 0
    elif p.slice[1].type == 'VERDADERO':
        p[0] = True
    elif p.slice[1].type == 'FALSO':
        p[0] = False
    else:
        p[0] = p[1]


# ==========================================
# 13. PRODUCCION VACIA
# ==========================================
def p_empty(p):
    "empty :"
    p[0] = None


# ==========================================
# 14. DETECCION DE ERRORES (Lo que pide el reporte)
# ==========================================
def p_error(p):
    if p:
        mensaje = f"Error sintáctico en línea {p.lineno}: token inesperado '{p.value}'"
        parser.errors.append(mensaje)
    else:
        parser.errors.append("Error sintáctico: fin inesperado del programa.")


# ==========================================
# 15. CONSTRUIR PARSER
# ==========================================
parser = yacc.yacc(
    start="programa",
    write_tables=False,
    debug=False
)


# ==========================================
# 16. FUNCION PRINCIPAL DE ANALISIS
# ==========================================
def analizar(codigo):
    global variables
    variables = {}  # Limpiamos variables en cada análisis

    lexer = build_lexer()
    parser.errors = []

    resultado = parser.parse(codigo, lexer=lexer)

    errores = list(lexer.errors)
    errores.extend(parser.errors)

    return resultado, errores