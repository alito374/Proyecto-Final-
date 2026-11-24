
# NOVACODE IDE

## 1. Descripción del proyecto

NovaCode es un lenguaje de programación educativo de autoría propia, diseñado para trabajar con instrucciones en español.

El proyecto incluye un entorno de desarrollo integrado (IDE) creado con PyQt6 y un analizador léxico y sintáctico implementado mediante la biblioteca PLY.

## 2. Objetivo general

Diseñar e implementar un lenguaje de programación propio que permita reconocer instrucciones, variables, operaciones matemáticas y estructuras de control mediante un analizador léxico y sintáctico.

## 3. Tecnologías utilizadas

- Python
- PyQt6
- Qt Designer
- PLY
- GitHub

## 4. Funciones principales

- Crear documentos nuevos.
- Abrir archivos con extensión `.nova`.
- Guardar programas.
- Copiar, cortar y pegar código.
- Buscar palabras dentro del editor.
- Analizar código fuente.
- Reconocer tokens.
- Detectar errores léxicos.
- Detectar errores sintácticos.

## 5. Estructura básica del lenguaje

Los programas de NovaCode comienzan con la palabra reservada `inicio` seguida de una llave de apertura `{`.

Al finalizar las instrucciones, se utiliza una llave de cierre `}` seguida de la palabra reservada `fin`.

Las instrucciones que lo requieren deben terminar con punto y coma.

Ejemplo:

```nova
inicio {
    edad = 20;
    mostrar("Hola NovaCode");
} fin
```

## 6. Requisitos

- Python 3 instalado.
- PyQt6.
- PLY.
- Sistema operativo compatible con Python y PyQt6.

## 7. Instalación y configuración

### 7.1. Descargar el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/alito374/Proyecto-Final-.git
```

Entrar a la carpeta del proyecto:

```bash
cd "Proyecto-Final-/Nova Code"
```

### 7.2. Instalar dependencias

Ejecutar:

```bash
pip3 install -r requirements.txt
```

### 7.3. Ejecutar NovaCode IDE

Ejecutar el siguiente comando:

```bash
python3 main.py
```

## 8. Archivos de prueba

El proyecto incluye dos programas de demostración:

- `correcto.nova`: contiene instrucciones válidas para comprobar el funcionamiento del analizador.
- `incorrecto.nova`: contiene errores intencionales para comprobar la detección de errores léxicos y sintácticos.

Ambos archivos pueden abrirse desde el editor NovaCode IDE para realizar las pruebas.

## 9. Alcance del proyecto

NovaCode permite realizar análisis léxico y sintáctico de programas escritos en su propio lenguaje.

El proyecto valida la estructura del código y detecta errores, pero no ejecuta las instrucciones como un lenguaje de programación interpretado.

## 10. Integrantes

Consultar la portada del reporte final para conocer los nombres de los integrantes y sus responsabilidades.
