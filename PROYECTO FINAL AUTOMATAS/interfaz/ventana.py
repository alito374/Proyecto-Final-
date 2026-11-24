from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QColor, QKeySequence, QShortcut, QTextCharFormat, QTextCursor
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
        self.txtBuscar.returnPressed.connect(self.buscar_texto)
        self.btnAnalizar.clicked.connect(self.analizar_codigo)
        self.tituloResultados.setReadOnly(True)
        self.editorCodigo.textChanged.connect(self.tituloResultados.clear)
        QShortcut(QKeySequence.StandardKey.Find, self).activated.connect(self.txtBuscar.setFocus)

    def copiar_texto(self):
        if self.editorCodigo.textCursor().hasSelection():
            self.editorCodigo.copy()
            self.statusbar.showMessage("Selección copiada.", 2500)

    def cortar_texto(self):
        if self.editorCodigo.textCursor().hasSelection():
            self.editorCodigo.cut()
            self.statusbar.showMessage("Selección cortada.", 2500)

    def pegar_texto(self):
        if self.editorCodigo.canPaste():
            self.editorCodigo.paste()
            self.statusbar.showMessage("Texto pegado.", 2500)

    def nuevo_archivo(self):
        if self.confirmar_cambios():
            self.editorCodigo.clear()
            self.editorCodigo.document().setModified(False)

    def confirmar_cambios(self):
        if not self.editorCodigo.document().isModified():
            return True
        botones = QMessageBox.StandardButton
        respuesta = QMessageBox.question(
            self, "Cambios sin guardar", "¿Quieres guardar los cambios del programa?",
            botones.Save | botones.Discard | botones.Cancel, botones.Save
        )
        if respuesta == botones.Save:
            return self.guardar_archivo()
        return respuesta == botones.Discard

    def closeEvent(self, evento):
        if self.confirmar_cambios():
            evento.accept()
        else:
            evento.ignore()

    def abrir_archivo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo de ALMA",
            "",
            "Archivos ALMA (*.alma);;Archivos de texto (*.txt);;Todos los archivos (*)"
        )

        if ruta_archivo and self.confirmar_cambios():
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()

                self.editorCodigo.setPlainText(contenido)
                self.editorCodigo.document().setModified(False)

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

                self.editorCodigo.document().setModified(False)
                QMessageBox.information(
                    self,
                    "Archivo guardado",
                    "El programa se guardó correctamente."
                )
                return True

            except (OSError, UnicodeError) as error:
                QMessageBox.critical(
                    self,
                    "Error al guardar",
                    "No se pudo guardar el archivo:\n{error}"
                )

        return False

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

        else:
            self.editorCodigo.setFocus()

    def analizar_codigo(self):
        codigo = self.editorCodigo.toPlainText()
        self.tituloResultados.clear()
        tokens_encontrados = []

        if not codigo.strip():
            valido = False
            mensaje = "Escribe un programa antes de analizar."
        else:
            valido, resultado = analizar(codigo, tokens_encontrados=tokens_encontrados)
            if valido:
                mensaje = "Análisis léxico correcto.\nAnálisis sintáctico correcto.\nPrograma ALMA válido."
            else:
                mensaje = "Se encontraron errores:\n" + "\n".join(resultado)

        formato = QTextCharFormat()
        formato.setForeground(QColor("#166534" if valido else "#9F1239"))
        cursor = QTextCursor(self.tituloResultados.document())
        cursor.insertText(mensaje, formato)

        if codigo.strip():
            filas = [
                f"{linea}:{columna}  {tipo:<18}  {valor!r}"
                for linea, columna, tipo, valor in tokens_encontrados
            ]
            listado = "\n".join(filas) if filas else "No se reconocieron tokens."
            formato.setForeground(QColor("#202836"))
            cursor.insertText(
                f"\n\nTokens reconocidos ({len(filas)})\nLínea:columna  Tipo  Valor\n{listado}",
                formato,
            )



