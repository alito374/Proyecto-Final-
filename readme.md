
# NOVACODE IDE

## Descripción

NovaCode es un lenguaje de programación educativo de
autoría propia, diseñado para trabajar con instrucciones
en español.

El proyecto incluye un editor de código desarrollado
con PyQt6 y un motor de análisis léxico y sintáctico
implementado con la librería PLY.

## Objetivo general

Diseñar e implementar un lenguaje de programación propio
que permita reconocer instrucciones, variables, operaciones
matemáticas y estructuras de control.

## Tecnologías utilizadas

- Python
- PyCharm
- PyQt6
- Qt Designer
- PLY
- GitHub

## Funciones principales

- Crear documentos.
- Abrir archivos .nova.
- Guardar programas.
- Copiar texto.
- Cortar texto.
- Pegar texto.
- Buscar palabras.
- Analizar código.
- Detectar errores léxicos.
- Detectar errores sintácticos.

## Instalación

Clonar el repositorio:

git clone URL_DE_TU_REPOSITORIO

Entrar a la carpeta:

cd NovaCode

Instalar dependencias:

pip install -r requirements.txt

Ejecutar:

python main.py

## Estructura del lenguaje

Todo programa debe comenzar con:

inicio {

Y finalizar con:

} fin

Las instrucciones deben terminar con punto y coma.

## Ejemplo

inicio {
    edad = 20;
    mostrar("Hola NovaCode");
} fin

## Integrantes

- Integrante 1: Analizador léxico.
- Integrante 2: Analizador sintáctico.
- Integrante 3: Interfaz gráfica e integración.

## Alcance

NovaCode valida la estructura léxica y sintáctica
de los programas escritos en su propio lenguaje.
No incluye ejecución de instrucciones.
