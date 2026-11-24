from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QTextDocument, QColor
from PyQt6 import uic
from analizador.parser import analizar


class VentanaALMA(QMainWindow):


    def __init__(self):
        super().__init__()

        ruta = Path(__file__).resolve().parent / "diseño.ui"
        uic.loadUi(str(ruta), self)

        # Conectar los botones
        self.btnCopiar.clicked.connect(self.copiar_texto)
        self.btnCortar.clicked.connect(self.cortar_texto)
        self.btnPegar.clicked.connect(self.pegar_texto)
        self.btnNuevo.clicked.connect(self.nuevo_archivo)
        self.btnAbrir.clicked.connect(self.abrir_archivo)
        self.btnGuardar.clicked.connect(self.guardar_archivo)
        self.btnBuscar.clicked.connect(self.buscar_texto)
        self.btnAnalizar.clicked.connect(self.analizar_codigo)
        self.tituloResultados.setReadOnly(True)

    def copiar_texto(self):
        self.editorCodigo.copy()

    def cortar_texto(self):
        self.editorCodigo.cut()

    def pegar_texto(self):
        self.editorCodigo.paste()

    def nuevo_archivo(self):
        self.editorCodigo.clear()

    def abrir_archivo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo de ALMA",
            "",
            "Archivos ALMA (*.alma);;Archivos de texto (*.txt);;Todos los archivos (*)"
        )

        if ruta_archivo:
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()

                self.editorCodigo.setPlainText(contenido)

            except (OSError, UnicodeError) as error:
                QMessageBox.critical(
                    self,
                    "Error al abrir",
                    f"No se pudo abrir el archivo:\n{error}"
                )

    def guardar_archivo(self):
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar programa ALMA",
            "",
            "Archivos ALMA (*.alma);;Archivos de texto (*.txt)"
        )

        if ruta_archivo:
            try:
                ruta = Path(ruta_archivo)

                if not ruta.suffix:
                    ruta = ruta.with_suffix(".alma")

                contenido = self.editorCodigo.toPlainText()

                with open(ruta, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)

                QMessageBox.information(
                    self,
                    "Archivo guardado",
                    "El programa se guardó correctamente."
                )

            except (OSError, UnicodeError) as error:
                QMessageBox.critical(
                    self,
                    "Error al guardar",
                    "No se pudo guardar el archivo:\n{error}"
                )

    def buscar_texto(self):
        palabra = self.txtBuscar.text().strip()

        if not palabra:
            QMessageBox.information(
                self,
                "Buscar",
                "Escribe una palabra para buscar."
            )
            return

        encontrado = self.editorCodigo.find(palabra)

        if not encontrado:
            cursor = self.editorCodigo.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            self.editorCodigo.setTextCursor(cursor)

            encontrado = self.editorCodigo.find(palabra)

        if not encontrado:
            QMessageBox.information(
                self,
                "Buscar",
                f"No se encontró '{palabra}' en el código."
            )

    def analizar_codigo(self):
        codigo = self.editorCodigo.toPlainText()

        self.tituloResultados.clear()

        if not codigo.strip():
            self.tituloResultados.setTextColor(
                QColor("#FF7777")
            )
            self.tituloResultados.append(
                "Escribe un programa antes de analizar."
            )
            return

        valido, resultado = analizar(codigo)

        if valido:
            self.tituloResultados.setTextColor(
                QColor("#70D890")
            )
            self.tituloResultados.append(
                "Análisis léxico correcto."
            )
            self.tituloResultados.append(
                "Análisis sintáctico correcto."
            )
            self.tituloResultados.append(
                "Programa ALMA válido."
            )

        else:
            self.tituloResultados.setTextColor(
                QColor("#FF7777")
            )
            self.tituloResultados.append(
                "Se encontraron errores:"
            )

            for error in resultado:
                self.tituloResultados.append(error)



