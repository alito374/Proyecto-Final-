
"""
NOVACODE - ANALIZADOR LEXICO
Desarrollado con Python y PLY.
Responsable: Integrante 1
"""

import ply.lex as lex

# ==========================================
# 1. PALABRAS RESERVADAS
# ==========================================

reserved = {
    "inicio": "INICIO",
    "fin": "FIN",
    "mostrar": "MOSTRAR",
    "si": "SI",
    "sino": "SINO",
    "mientras": "MIENTRAS",
    "verdadero": "VERDADERO",
    "falso": "FALSO"
}

# ==========================================
# 2. LISTA DE TOKENS
# ==========================================

tokens = [
    "IDENTIFICADOR",
    "NUMERO",
    "CADENA",

    "MAS",
    "MENOS",
    "POR",
    "DIVIDIDO",

    "IGUAL",
    "IGUALIGUAL",
    "DIFERENTE",

    "MENOR",
    "MENORIGUAL",
    "MAYOR",
    "MAYORIGUAL",

    "PARENTESIS_IZQ",
    "PARENTESIS_DER",

    "LLAVE_IZQ",
    "LLAVE_DER",

    "PUNTO_COMA"
] + list(reserved.values())

# ==========================================
# 3. EXPRESIONES REGULARES
# ==========================================

t_IGUALIGUAL = r"=="
t_DIFERENTE = r"!="
t_MENORIGUAL = r"<="
t_MAYORIGUAL = r">="

t_IGUAL = r"="
t_MENOR = r"<"
t_MAYOR = r">"

t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIVIDIDO = r"/"

t_PARENTESIS_IZQ = r"\("
t_PARENTESIS_DER = r"\)"

t_LLAVE_IZQ = r"\{"
t_LLAVE_DER = r"\}"

t_PUNTO_COMA = r";"

# Espacios ignorados
t_ignore = " \t\r"

# ==========================================
# 4. RECONOCER COMENTARIOS
# ==========================================

def t_COMENTARIO(t):
    r"//[^\n]*"
    pass

# ==========================================
# 5. RECONOCER CADENAS
# ==========================================

def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

# ==========================================
# 6. RECONOCER NUMEROS
# ==========================================

def t_NUMERO(t):
    r"\d+(\.\d+)?"

    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)

    return t

# ==========================================
# 7. RECONOCER IDENTIFICADORES
# ==========================================

def t_IDENTIFICADOR(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"

    t.type = reserved.get(t.value, "IDENTIFICADOR")

    return t

# ==========================================
# 8. CONTAR LINEAS
# ==========================================

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# ==========================================
# 9. DETECTAR ERRORES LEXICOS
# ==========================================

def t_error(t):

    mensaje = (
        f"Error léxico en línea {t.lineno}: "
        f"carácter no reconocido '{t.value[0]}'"
    )

    t.lexer.errors.append(mensaje)

    t.lexer.skip(1)

# ==========================================
# 10. CONSTRUIR ANALIZADOR
# ==========================================

def build_lexer():

    lexer = lex.lex()

    lexer.errors = []

    return lexer


# ==========================================
# 11. PRUEBA INDIVIDUAL
# ==========================================

if __name__ == "__main__":

    codigo = """
    inicio {
        edad = 20;
        mostrar("Hola NovaCode");
    } fin
    """

    analizador = build_lexer()

    analizador.input(codigo)

    print("TOKENS RECONOCIDOS:")

    for token in analizador:
        print(token)

    print("\nERRORES:")

    for error in analizador.errors:
        print(error)
