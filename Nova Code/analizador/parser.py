
"""
NOVACODE - ANALIZADOR SINTACTICO
Desarrollado con Python y PLY.
Responsable: Integrante 2
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

    p[0] = None


# ==========================================
# 5. INSTRUCCION MOSTRAR
# ==========================================

def p_instruccion_mostrar(p):
    "instruccion : MOSTRAR PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA"

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

    p[0] = None


# ==========================================
# 10. NUMEROS NEGATIVOS
# ==========================================

def p_expresion_unaria(p):
    "expresion : MENOS expresion %prec UMINUS"

    p[0] = None


# ==========================================
# 11. EXPRESIONES ENTRE PARENTESIS
# ==========================================

def p_expresion_parentesis(p):
    "expresion : PARENTESIS_IZQ expresion PARENTESIS_DER"

    p[0] = None


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

    p[0] = None


# ==========================================
# 13. PRODUCCION VACIA
# ==========================================

def p_empty(p):
    "empty :"

    p[0] = None


# ==========================================
# 14. DETECCION DE ERRORES
# ==========================================

def p_error(p):

    if p:

        parser.errors.append(
            f"Error sintáctico en línea {p.lineno}: "
            f"token inesperado '{p.value}'"
        )

    else:

        parser.errors.append(
            "Error sintáctico: fin inesperado del programa."
        )


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

    lexer = build_lexer()

    parser.errors = []

    resultado = parser.parse(
        codigo,
        lexer=lexer
    )

    errores = list(lexer.errors)

    errores.extend(parser.errors)

    return resultado, errores


# ==========================================
# 17. PRUEBA INDIVIDUAL
# ==========================================

if __name__ == "__main__":

    codigo = """
    inicio {
        edad = 20;
        resultado = edad + 5;
        mostrar("Hola NovaCode");

        si (edad >= 18) {
            mostrar("Mayor de edad");
        }

    } fin
    """

    resultado, errores = analizar(codigo)

    if errores:

        print("CODIGO INVALIDO")

        for error in errores:
            print(error)

    else:

        print("CODIGO VALIDO")
        print(resultado)
