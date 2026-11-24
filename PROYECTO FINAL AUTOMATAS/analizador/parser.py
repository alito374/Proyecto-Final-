import ply.yacc as yacc

if __package__:
    from .lexer import tokens, lexer, errores_lexicos
else:
    from lexer import tokens, lexer, errores_lexicos


# Guardar los errores encontrados
errores = []


# Prioridad de las operaciones matemáticas
precedence = (
    ("nonassoc", "MAYOR", "MENOR", "MAYOR_IGUAL", "MENOR_IGUAL", "COMPARACION", "DIFERENTE"),
    ("left", "MAS", "MENOS"),
    ("left", "MULTIPLICACION", "DIVISION"),
    ("right", "NEGATIVO"),
)


# Estructura principal de ALMA
def p_programa(p):
    "programa : DESPIERTA instrucciones DESCANSA"
    p[0] = ("programa", p[2])


# Una o varias instrucciones
def p_instrucciones_varias(p):
    "instrucciones : instrucciones instruccion"
    p[1].append(p[2])
    p[0] = p[1]


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


def p_instruccion_escucha(p):
    "instruccion : ESCUCHA IDENTIFICADOR"
    p[0] = ("escucha", p[2])


def p_bloque(p):
    """bloque : LLAVE_ABRE instrucciones LLAVE_CIERRA
              | LLAVE_ABRE LLAVE_CIERRA"""
    p[0] = p[2] if len(p) == 4 else []


def p_instruccion_imagina(p):
    """instruccion : IMAGINA expresion bloque
                   | IMAGINA expresion bloque DEOTROMODO bloque"""
    alternativa = p[5] if len(p) == 6 else []
    p[0] = ("imagina", p[2], p[3], alternativa)


def p_instruccion_ciclo(p):
    """instruccion : PERSISTE expresion bloque
                   | REVIVE expresion bloque"""
    p[0] = (p[1].lower(), p[2], p[3])


def p_instruccion_crea(p):
    "instruccion : CREA IDENTIFICADOR PARENTESIS_ABRE parametros PARENTESIS_CIERRA bloque"
    p[0] = ("crea", p[2], p[4], p[6])


def p_instruccion_entrega(p):
    "instruccion : ENTREGA expresion"
    p[0] = ("entrega", p[2])


def p_instruccion_llamada(p):
    "instruccion : llamada"
    p[0] = p[1]


def p_llamada(p):
    "llamada : ENLAZA IDENTIFICADOR PARENTESIS_ABRE argumentos PARENTESIS_CIERRA"
    p[0] = ("enlaza", p[2], p[4])


def p_listas_vacias(p):
    """parametros :
       argumentos :"""
    p[0] = []


def p_parametros(p):
    """parametros : nombres
       nombres : IDENTIFICADOR
               | nombres COMA IDENTIFICADOR"""
    if len(p) == 2:
        p[0] = [p[1]] if p.slice[1].type == "IDENTIFICADOR" else p[1]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_argumentos(p):
    """argumentos : valores
       valores : expresion
               | valores COMA expresion"""
    if len(p) == 2:
        p[0] = [p[1]] if p.slice[1].type == "expresion" else p[1]
    else:
        p[1].append(p[3])
        p[0] = p[1]


# Operaciones matemáticas
def p_expresion_operacion(p):
    """expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion COMPARACION expresion
                 | expresion DIFERENTE expresion"""
    p[0] = ("operacion", p[2], p[1], p[3])


def p_expresion_negativa(p):
    "expresion : MENOS expresion %prec NEGATIVO"
    p[0] = ("negativo", p[2])


def p_expresion_booleana(p):
    """expresion : CIERTO
                 | FINGIDO"""
    p[0] = ("booleano", p[1] == "CIERTO")


def p_expresion_llamada(p):
    "expresion : llamada"
    p[0] = p[1]


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
        columna = p.lexpos - lexer.lexdata.rfind("\n", 0, p.lexpos)
        mensaje = (
            f"Error sintáctico en la línea {p.lineno}, columna {columna}: "
            f"se encontró {p.value!r} ({p.type}) en una posición inesperada."
        )
    else:
        mensaje = (
            f"Error sintáctico en la línea {lexer.lineno}: fin del código inesperado. "
            "Revisa que las instrucciones estén completas y que el programa termine con DESCANSA."
        )

    errores.append(mensaje)


# Construir el analizador sintáctico
parser = yacc.yacc(write_tables=False, debug=False)


# Analizar un programa ALMA

def analizar(codigo, *, tokens_encontrados=None):
    errores.clear()
    errores_lexicos.clear()
    lexer.lineno = 1

    codigo = codigo.replace("\r\n", "\n").replace("\r", "\n")

    def leer_token():
        token = lexer.token()
        if token is not None:
            columna = token.lexpos - codigo.rfind("\n", 0, token.lexpos)
            tokens_encontrados.append((token.lineno, columna, token.type, token.value))
        return token

    lector = leer_token if tokens_encontrados is not None else lexer.token
    try:
        resultado = parser.parse(codigo, lexer=lexer, tokenfunc=lector)
    except ValueError:
        return False, errores_lexicos + [
            f"Error léxico en la línea {lexer.lineno}: número fuera del rango admitido."
        ]

    if errores_lexicos or errores:
        return False, errores_lexicos + errores

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

