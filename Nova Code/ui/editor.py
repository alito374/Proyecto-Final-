
"""
NOVACODE IDE
INTERFAZ GRAFICA CON PYQT6
Responsable: Integrante 3
"""

import sys
from pathlib import Path

from PyQt6 import uic

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox
)

from PyQt6.QtGui import QAction, QFont

from parser import analizar


# ==========================================
# RUTA DE LA INTERFAZ
# ==========================================

UI_PATH = Path(__file__).with_name("novacode.ui")


# ==========================================
# CLASE PRINCIPAL
# ==========================================

class NovaCodeIDE(QMainWindow):

    def __init__(self):

        super().__init__()

        # Cargar interfaz Qt Designer
        uic.loadUi(str(UI_PATH), self)

        self.archivo_actual = None

        # Configurar editor
        self.editorCodigo.setFont(
            QFont("Consolas", 11)
        )

        # Conectar botones
        self.btnNuevo.clicked.connect(
            self.nuevo_archivo
        )

        self.btnAbrir.clicked.connect(
            self.abrir_archivo
        )

        self.btnGuardar.clicked.connect(
            self.guardar_archivo
        )

        self.btnCopiar.clicked.connect(
            self.editorCodigo.copy
        )

        self.btnCortar.clicked.connect(
            self.editorCodigo.cut
        )

        self.btnPegar.clicked.connect(
            self.editorCodigo.paste
        )

        self.btnBuscar.clicked.connect(
            self.buscar_texto
        )

        self.btnAnalizar.clicked.connect(
            self.analizar_codigo
        )

        # Crear menú superior
        self.crear_menu()

    # ======================================
    # MENU
    # ======================================

    def crear_menu(self):

        menu_archivo = self.menuBar().addMenu(
            "Archivo"
        )

        accion_nuevo = QAction("Nuevo", self)

        accion_nuevo.triggered.connect(
            self.nuevo_archivo
        )

        menu_archivo.addAction(accion_nuevo)

        accion_abrir = QAction("Abrir", self)

        accion_abrir.triggered.connect(
            self.abrir_archivo
        )

        menu_archivo.addAction(accion_abrir)

        accion_guardar = QAction("Guardar", self)

        accion_guardar.triggered.connect(
            self.guardar_archivo
        )

        menu_archivo.addAction(accion_guardar)

        menu_editar = self.menuBar().addMenu(
            "Editar"
        )

        acciones = [
            ("Copiar", self.editorCodigo.copy),
            ("Cortar", self.editorCodigo.cut),
            ("Pegar", self.editorCodigo.paste)
        ]

        for nombre, funcion in acciones:

            accion = QAction(nombre, self)

            accion.triggered.connect(funcion)

            menu_editar.addAction(accion)

    # ======================================
    # NUEVO DOCUMENTO
    # ======================================

    def nuevo_archivo(self):

        self.editorCodigo.clear()

        self.salidaResultados.clear()

        self.archivo_actual = None

        self.lblEstado.setText(
            "Estado: nuevo documento"
        )

    # ======================================
    # ABRIR DOCUMENTO
    # ======================================

    def abrir_archivo(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo NovaCode",
            "",
            "NovaCode (*.nova);;Texto (*.txt);;Todos (*.*)"
        )

        if ruta:

            try:

                contenido = Path(ruta).read_text(
                    encoding="utf-8"
                )

                self.editorCodigo.setPlainText(
                    contenido
                )

                self.archivo_actual = ruta

                self.statusbar.showMessage(
                    "Archivo abierto correctamente"
                )

            except OSError as error:

                QMessageBox.critical(
                    self,
                    "Error al abrir",
                    str(error)
                )

    # ======================================
    # GUARDAR DOCUMENTO
    # ======================================

    def guardar_archivo(self):

        ruta = self.archivo_actual

        if not ruta:

            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo NovaCode",
                "programa.nova",
                "NovaCode (*.nova)"
            )

        if ruta:

            try:

                contenido = (
                    self.editorCodigo.toPlainText()
                )

                Path(ruta).write_text(
                    contenido,
                    encoding="utf-8"
                )

                self.archivo_actual = ruta

                self.statusbar.showMessage(
                    "Archivo guardado correctamente"
                )

            except OSError as error:

                QMessageBox.critical(
                    self,
                    "Error al guardar",
                    str(error)
                )

    # ======================================
    # BUSCAR PALABRAS
    # ======================================

    def buscar_texto(self):

        palabra = self.txtBuscar.text()

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

        encontrado = self.editorCodigo.find(
            palabra
        )

        if encontrado:

            self.salidaResultados.setPlainText(
                f"Palabra encontrada: {palabra}"
            )

        else:

            self.salidaResultados.setPlainText(
                f"No se encontró: {palabra}"
            )

    # ======================================
    # ANALIZAR CODIGO
    # ======================================

    def analizar_codigo(self):

        codigo = self.editorCodigo.toPlainText()

        if not codigo.strip():

            self.salidaResultados.setPlainText(
                "No existe código para analizar."
            )

            self.lblEstado.setText(
                "Estado: sin código"
            )

            return

        try:

            resultado, errores = analizar(codigo)

            if errores:

                texto = (
                    "ANALISIS FINALIZADO: "
                    "SE ENCONTRARON ERRORES\n\n"
                )

                for error in errores:

                    texto += "• " + error + "\n"

                self.lblEstado.setText(
                    "Estado: Código inválido"
                )

            else:

                texto = (
                    "ANALISIS EXITOSO\n\n"
                    "Análisis léxico: correcto\n"
                    "Análisis sintáctico: correcto\n"
                    "Estructura del programa: válida\n\n"
                    + str(resultado)
                )

                self.lblEstado.setText(
                    "Estado: Código válido"
                )

            self.salidaResultados.setPlainText(
                texto
            )

        except Exception as error:

            self.lblEstado.setText(
                "Estado: error del analizador"
            )

            self.salidaResultados.setPlainText(
                f"Error interno durante el análisis:\n{error}"
            )


# ==========================================
# INICIAR APLICACION
# ==========================================

def main():

    app = QApplication(sys.argv)

    ventana = NovaCodeIDE()

    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()
