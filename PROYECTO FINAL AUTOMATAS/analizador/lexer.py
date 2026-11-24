
import ply.lex as lex
# Lista para guardar los errores léxicos
errores_lexicos = []

# Palabras reservadas de nuestro lenguaje ALMA
reservadas = {
    "DESPIERTA": "DESPIERTA",
    "DESCANSA": "DESCANSA",
    "ATESORA": "ATESORA",
    "CUENTAME": "CUENTAME",
    "ESCUCHA": "ESCUCHA",
    "IMAGINA": "IMAGINA",
    "DEOTROMODO": "DEOTROMODO",
    "PERSISTE": "PERSISTE",
    "REVIVE": "REVIVE",
    "CIERTO": "CIERTO",
    "FINGIDO": "FINGIDO",
    "CREA": "CREA",
    "ENTREGA": "ENTREGA",
    "ENLAZA": "ENLAZA"
}

# Tokens que reconoce ALMA
tokens = (
    "IDENTIFICADOR",
    "NUMERO",
    "TEXTO",
    "IGUAL",
    "MAS",
    "MENOS",
    "MULTIPLICACION",
    "DIVISION",
    "MAYOR",
    "MENOR",
    "MAYOR_IGUAL",
    "MENOR_IGUAL",
    "COMPARACION",
    "DIFERENTE",
    "PARENTESIS_ABRE",
    "PARENTESIS_CIERRA",
    "LLAVE_ABRE",
    "LLAVE_CIERRA",
    "COMA"
) + tuple(reservadas.values())

# Símbolos y operadores
t_MAS = r"\+"
t_MENOS = r"-"
t_MULTIPLICACION = r"\*"
t_DIVISION = r"/"

t_MAYOR_IGUAL = r">="
t_MENOR_IGUAL = r"<="
t_COMPARACION = r"=="
t_DIFERENTE = r"!="

t_IGUAL = r"="
t_MAYOR = r">"
t_MENOR = r"<"

t_PARENTESIS_ABRE = r"\("
t_PARENTESIS_CIERRA = r"\)"
t_LLAVE_ABRE = r"\{"
t_LLAVE_CIERRA = r"\}"
t_COMA = r","

# Ignorar espacios y tabulaciones
t_ignore = " \t"


# Reconocer números enteros y decimales
def t_NUMERO(t):
    r"\d+(\.\d+)?"
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# Reconocer textos entre comillas
def t_TEXTO(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t


# Reconocer variables y palabras reservadas
def t_IDENTIFICADOR(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reservadas.get(t.value, "IDENTIFICADOR")
    return t


# Reconocer saltos de línea
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Reconocer comentarios de ALMA
def t_comentario(t):
    r"~[^\n]*"
    pass


# Mostrar errores léxicos
def t_error(t):
    mensaje = (
        f"Error léxico en la línea {t.lexer.lineno}: "
        f"carácter no reconocido '{t.value[0]}'"
    )

    errores_lexicos.append(mensaje)
    t.lexer.skip(1)


# Crear el analizador léxico
lexer = lex.lex()


# Prueba de nuestro lenguaje
if __name__ == "__main__":
    codigo = """DESPIERTA
ATESORA nombre = "ALMA"
ATESORA edad = 20
CUENTAME nombre
CUENTAME edad
DESCANSA"""

    lexer.input(codigo)

    for token in lexer:
        print(token)
