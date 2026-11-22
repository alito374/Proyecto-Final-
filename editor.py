
"""
NOVACODE IDE
Interfaz gráfica moderna con PyQt6, resaltado de sintaxis
y botones con efectos de iluminación.
"""

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt, QRegularExpression, QEvent
from PyQt6.QtGui import (
    QAction, QFont, QColor, QTextCharFormat, QSyntaxHighlighter
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QGraphicsDropShadowEffect, QPushButton
)

from parser import analizar

UI_PATH = Path(__file__).with_name("novacode.ui")


# ==========================================================
# RESALTADO DE SINTAXIS
# ==========================================================

class NovaHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        def add(pattern, color, bold=False, italic=False):
            formato = QTextCharFormat()
            formato.setForeground(QColor(color))

            if bold:
                formato.setFontWeight(QFont.Weight.Bold)

            if italic:
                formato.setFontItalic(True)

            self.rules.append((QRegularExpression(pattern), formato))

        add(r"\b(inicio|fin|si|sino|mientras)\b", "#C4A7FF", True)
        add(r"\b(mostrar)\b", "#70D6FF", True)
        add(r"\b(verdadero|falso)\b", "#F6C177", True)
        add(r'"([^"\\]|\\.)*"', "#A6E3A1")
        add(r"\b\d+(\.\d+)?\b", "#F9C74F")
        add(r"\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*=)", "#7DCFFF")
        add(r"==|!=|<=|>=|[=+\-*/<>]", "#FF8FAB", True)
        add(r"[{}();]", "#F2A2E8", True)
        add(r"//[^\n]*", "#8292A2", italic=True)

    def highlightBlock(self, text):
        for expresion, formato in self.rules:
            coincidencias = expresion.globalMatch(text)

            while coincidencias.hasNext():
                coincidencia = coincidencias.next()
                self.setFormat(
                    coincidencia.capturedStart(),
                    coincidencia.capturedLength(),
                    formato
                )


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================

class NovaCodeIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(str(UI_PATH), self)

        self.setWindowTitle("NOVACODE IDE")
        self.setMinimumSize(900, 650)

        self.archivo_actual = None

        # Aplicar estilos después de cargar el archivo UI.
        self.setStyleSheet(self.estilo_general())

        # Quitar estilos individuales del diseñador que puedan
        # impedir que se apliquen los nuevos colores.
        widgets = [
            self.btnNuevo,
            self.btnAbrir,
            self.btnGuardar,
            self.btnCopiar,
            self.btnCortar,
            self.btnPegar,
            self.btnBuscar,
            self.btnAnalizar,
            self.editorCodigo,
            self.salidaResultados
        ]

        for widget in widgets:
            widget.setStyleSheet("")

        # Fuente del editor.
        self.editorCodigo.setFont(QFont("JetBrains Mono", 12))
        self.editorCodigo.setTabStopDistance(
            4 * self.editorCodigo.fontMetrics().horizontalAdvance(" ")
        )

        # Resaltador de sintaxis.
        self.highlighter = NovaHighlighter(
            self.editorCodigo.document()
        )

        # Colores individuales de los botones.
        self.configurar_botones()

        # Conectar botones.
        self.btnNuevo.clicked.connect(self.nuevo_archivo)
        self.btnAbrir.clicked.connect(self.abrir_archivo)
        self.btnGuardar.clicked.connect(self.guardar_archivo)

        self.btnCopiar.clicked.connect(self.editorCodigo.copy)
        self.btnCortar.clicked.connect(self.editorCodigo.cut)
        self.btnPegar.clicked.connect(self.editorCodigo.paste)

        self.btnBuscar.clicked.connect(self.buscar_texto)
        self.btnAnalizar.clicked.connect(self.analizar_codigo)

        self.txtBuscar.returnPressed.connect(self.buscar_texto)

        self.crear_menu()

        self.statusbar.showMessage("Listo · NovaCode IDE")
        self.lblEstado.setText("●  Listo para analizar tu código")

    # ======================================================
    # ESTILOS GENERALES
    # ======================================================

    def estilo_general(self):

        return """
        QMainWindow, QWidget {
            background-color: #111827;
            color: #E5E7EB;
            font-family: "Segoe UI";
            font-size: 10pt;
        }

        QLabel#titulo {
            color: #F8FAFC;
            font-size: 23pt;
            font-weight: 800;
            padding: 14px 8px 8px 8px;
        }

        QLabel#lblEditor, QLabel#lblResultados {
            color: #A5B4FC;
            font-size: 10pt;
            font-weight: 700;
            padding: 7px 2px;
        }

        QLineEdit {
            background-color: #1E293B;
            color: #F8FAFC;
            border: 1px solid #394B63;
            border-radius: 8px;
            padding: 10px 12px;
            selection-background-color: #7C3AED;
        }

        QLineEdit:focus {
            border: 1px solid #A78BFA;
        }

        QPlainTextEdit {
            background-color: #0B1220;
            color: #E2E8F0;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 12px;
            selection-background-color: #5B4B9A;
            selection-color: white;
        }

        QStatusBar {
            background-color: #0B1220;
            color: #94A3B8;
            border-top: 1px solid #263449;
        }

        QMenuBar {
            background-color: #0B1220;
            color: #CBD5E1;
            padding: 5px;
        }

        QMenuBar::item:selected {
            background-color: #4C1D95;
            border-radius: 5px;
        }

        QMenu {
            background-color: #1E293B;
            color: #E2E8F0;
            border: 1px solid #475569;
        }

        QMenu::item:selected {
            background-color: #4C1D95;
        }
        """

    # ======================================================
    # BOTONES CON COLORES Y EFECTOS
    # ======================================================

    def configurar_botones(self):

        colores = {
            "btnNuevo": ("#0F766E", "#14B8A6", "#5EEAD4"),
            "btnAbrir": ("#1D4ED8", "#3B82F6", "#93C5FD"),
            "btnGuardar": ("#15803D", "#22C55E", "#86EFAC"),
            "btnCopiar": ("#6D28D9", "#8B5CF6", "#C4B5FD"),
            "btnCortar": ("#BE185D", "#EC4899", "#F9A8D4"),
            "btnPegar": ("#A16207", "#EAB308", "#FDE047"),
            "btnBuscar": ("#0369A1", "#0EA5E9", "#7DD3FC"),
            "btnAnalizar": ("#6D28D9", "#A78BFA", "#DDD6FE")
        }

        for nombre, valores in colores.items():

            boton = getattr(self, nombre)

            normal, hover, brillo = valores

            boton.setCursor(Qt.CursorShape.PointingHandCursor)

            if nombre == "btnAnalizar":
                boton.setMinimumHeight(48)
                boton.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            else:
                boton.setMinimumHeight(38)
                boton.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))

            boton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {normal};
                    color: white;
                    border: 1px solid {normal};
                    border-radius: 10px;
                    padding: 9px 15px;
                    font-weight: bold;
                }}

                QPushButton:hover {{
                    background-color: {hover};
                    color: white;
                    border: 2px solid {brillo};
                    padding: 8px 14px;
                }}

                QPushButton:pressed {{
                    background-color: #312E81;
                    border: 2px solid white;
                    padding-top: 11px;
                }}

                QPushButton:disabled {{
                    background-color: #374151;
                    color: #9CA3AF;
                    border: 1px solid #4B5563;
                }}
            """)

            # Efecto de iluminación al pasar el cursor.
            efecto = QGraphicsDropShadowEffect(boton)
            efecto.setBlurRadius(0)
            efecto.setOffset(0, 0)
            efecto.setColor(QColor(brillo))

            boton.setGraphicsEffect(efecto)

            boton.installEventFilter(self)

            boton._efecto_brillo = efecto
            boton._color_brillo = QColor(brillo)

    # ======================================================
    # EVENTOS DE LOS BOTONES
    # ======================================================

    def eventFilter(self, objeto, evento):

        if isinstance(objeto, QPushButton):

            efecto = getattr(objeto, "_efecto_brillo", None)

            if efecto:

                if evento.type() == QEvent.Type.Enter:
                    efecto.setBlurRadius(28)
                    efecto.setOffset(0, 0)
                    efecto.setColor(objeto._color_brillo)

                elif evento.type() == QEvent.Type.Leave:
                    efecto.setBlurRadius(0)

        return super().eventFilter(objeto, evento)

    # ======================================================
    # MENÚ SUPERIOR
    # ======================================================

    def crear_menu(self):

        menu_archivo = self.menuBar().addMenu("Archivo")

        opciones_archivo = [
            ("Nuevo", self.nuevo_archivo),
            ("Abrir", self.abrir_archivo),
            ("Guardar", self.guardar_archivo)
        ]

        for nombre, funcion in opciones_archivo:
            accion = QAction(nombre, self)
            accion.triggered.connect(funcion)
            menu_archivo.addAction(accion)

        menu_editar = self.menuBar().addMenu("Editar")

        opciones_editar = [
            ("Copiar", self.editorCodigo.copy),
            ("Cortar", self.editorCodigo.cut),
            ("Pegar", self.editorCodigo.paste)
        ]

        for nombre, funcion in opciones_editar:
            accion = QAction(nombre, self)
            accion.triggered.connect(funcion)
            menu_editar.addAction(accion)

    # ======================================================
    # NUEVO ARCHIVO
    # ======================================================

    def nuevo_archivo(self):

        self.editorCodigo.clear()
        self.salidaResultados.clear()

        self.archivo_actual = None

        self.lblEstado.setText("●  Nuevo documento")
        self.lblEstado.setStyleSheet("color: #A5B4FC;")

        self.statusbar.showMessage("Documento nuevo")

    # ======================================================
    # ABRIR ARCHIVO
    # ======================================================

    def abrir_archivo(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo NovaCode",
            "",
            "NovaCode (*.nova);;Texto (*.txt);;Todos (*.*)"
        )

        if not ruta:
            return

        try:

            contenido = Path(ruta).read_text(encoding="utf-8")

            self.editorCodigo.setPlainText(contenido)
            self.archivo_actual = ruta

            self.lblEstado.setText("●  Archivo abierto")
            self.lblEstado.setStyleSheet("color: #60A5FA;")

            self.statusbar.showMessage(
                f"Abierto: {Path(ruta).name}"
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Error al abrir",
                str(error)
            )

    # ======================================================
    # GUARDAR ARCHIVO
    # ======================================================

    def guardar_archivo(self):

        ruta = self.archivo_actual

        if not ruta:

            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo NovaCode",
                "programa.nova",
                "NovaCode (*.nova)"
            )

        if not ruta:
            return

        try:

            Path(ruta).write_text(
                self.editorCodigo.toPlainText(),
                encoding="utf-8"
            )

            self.archivo_actual = ruta

            self.lblEstado.setText("●  Cambios guardados")
            self.lblEstado.setStyleSheet("color: #86EFAC;")

            self.statusbar.showMessage(
                f"Guardado: {Path(ruta).name}"
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Error al guardar",
                str(error)
            )

    # ======================================================
    # BUSCAR TEXTO
    # ======================================================

    def buscar_texto(self):

        palabra = self.txtBuscar.text().strip()

        if not palabra:

            self.salidaResultados.setPlainText(
                "Escribe una palabra para buscar."
            )
            return

        cursor = self.editorCodigo.textCursor()

        cursor.movePosition(
            cursor.MoveOperation.Start
        )

        self.editorCodigo.setTextCursor(cursor)

        if self.editorCodigo.find(palabra):

            self.salidaResultados.setPlainText(
                f"✓  Palabra encontrada: {palabra}"
            )

            self.lblEstado.setText("●  Coincidencia encontrada")
            self.lblEstado.setStyleSheet("color: #86EFAC;")

            self.statusbar.showMessage(
                f"Coincidencia encontrada: {palabra}"
            )

        else:

            self.salidaResultados.setPlainText(
                f"No se encontró: {palabra}"
            )

            self.lblEstado.setText("●  Sin coincidencias")
            self.lblEstado.setStyleSheet("color: #FBBF24;")

            self.statusbar.showMessage(
                "Búsqueda finalizada"
            )

    # ======================================================
    # ANALIZAR CÓDIGO
    # ======================================================

    def analizar_codigo(self):

        codigo = self.editorCodigo.toPlainText()

        if not codigo.strip():

            self.salidaResultados.setPlainText(
                "No hay código para analizar."
            )

            self.lblEstado.setText("●  Sin código")
            self.lblEstado.setStyleSheet("color: #FBBF24;")

            return

        try:

            resultado, errores = analizar(codigo)

            if errores:

                texto = (
                    "✕  ANÁLISIS FINALIZADO · "
                    "SE ENCONTRARON ERRORES\n\n"
                )

                texto += "\n".join(
                    f"• {error}" for error in errores
                )

                self.lblEstado.setText("●  Código inválido")
                self.lblEstado.setStyleSheet(
                    "color: #F87171; font-weight: bold;"
                )

            else:

                texto = (
                    "✓  ANÁLISIS EXITOSO\n\n"
                    "Análisis léxico: correcto\n"
                    "Análisis sintáctico: correcto\n"
                    "Estructura del programa: válida\n\n"
                    f"{resultado}"
                )

                self.lblEstado.setText("●  Código válido")
                self.lblEstado.setStyleSheet(
                    "color: #86EFAC; font-weight: bold;"
                )

            self.salidaResultados.setPlainText(texto)

            self.statusbar.showMessage(
                "Análisis terminado"
            )

        except Exception as error:

            self.lblEstado.setText("●  Error del analizador")
            self.lblEstado.setStyleSheet(
                "color: #F87171; font-weight: bold;"
            )

            self.salidaResultados.setPlainText(
                f"Error interno durante el análisis:\n{error}"
            )


# ==========================================================
# EJECUCIÓN
# ==========================================================

def main():

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ventana = NovaCodeIDE()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
