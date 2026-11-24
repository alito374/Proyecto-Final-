# ALMA

ALMA es un lenguaje educativo con instrucciones en español. El editor de Qt Designer permite escribir y guardar programas. PLY revisa su vocabulario y su estructura, y el editor muestra el resultado del análisis. La entrega cubre la validación léxica y sintáctica.

## Ejecutar en PyCharm

1. Clona el repositorio desde **Get from VCS** y abre la carpeta clonada.
2. En **Settings → Project → Python Interpreter**, selecciona o crea un entorno virtual con Python 3.14.
3. Abre la terminal de PyCharm con el entorno activado e instala las dependencias.

   ```powershell
   python -m pip install -r "PROYECTO FINAL AUTOMATAS/requirements.txt"
   ```

4. Abre `PROYECTO FINAL AUTOMATAS/main.py` y elige **Run 'main'**. También puedes ejecutarlo desde la raíz.

   ```powershell
   python "PROYECTO FINAL AUTOMATAS/main.py"
   ```

5. Abre los dos archivos en `ejemplos/` y pulsa **Analizar**. `valido.alma` debe pasar ambos análisis. `invalido.alma` tiene un carácter desconocido y una expresión incompleta.

## Reglas de ALMA

El programa empieza con `DESPIERTA`, contiene al menos una instrucción y termina con `DESCANSA`. Las palabras reservadas se escriben en mayúsculas. Las instrucciones empiezan con una palabra reservada. Los saltos de línea separan visualmente el código y `~` inicia un comentario hasta el final de la línea.

| Instrucción | Forma |
| --- | --- |
| Guardar un valor | `ATESORA total = 2 + 3` |
| Mostrar un valor | `CUENTAME total` |
| Leer un dato | `ESCUCHA nombre` |
| Condición | `IMAGINA total >= 5 { CUENTAME total }` con `DEOTROMODO { ... }` opcional |
| Repetir mientras se cumpla una condición | `PERSISTE condicion { ... }` |
| Repetir cierta cantidad de veces | `REVIVE 3 { ... }` |
| Declarar una función | `CREA sumar(a, b) { ENTREGA a + b }` |
| Llamar una función | `ENLAZA sumar(2, 3)`, también dentro de una expresión |

Las expresiones incluyen números, textos entre comillas dobles, variables y los valores `CIERTO` y `FINGIDO`. Los paréntesis agrupan expresiones. De mayor a menor prioridad se aplican el signo menos, la multiplicación y división, la suma y resta, y las comparaciones. Para combinar comparaciones utiliza paréntesis explícitos.

## Archivos del repositorio

- `PROYECTO FINAL AUTOMATAS/main.py` abre el editor de ALMA.
- `analizador/lexer.py` define tokens y expresiones regulares. `analizador/parser.py` define las producciones.
- `interfaz/diseño.ui` es el diseño activo de Qt Designer. `interfaz/ventana.py` conecta sus controles.
- `diseño_respaldo.ui` es el respaldo de la interfaz. `Nova Code/` e `interfaz2-Menugrafico/` son proyectos separados del arranque de ALMA.
