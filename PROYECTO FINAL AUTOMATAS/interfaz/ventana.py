from pathlib import Path
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class VentanaALMA(QMainWindow):

    def __init__(self):
        super().__init__()

        ruta = Path(__file__).resolve().parent / "diseño.ui"
        uic.loadUi(str(ruta), self)

        # Conectar los botones
        self.btnCopiar.clicked.connect(self.copiar_texto)
        self.btnCortar.clicked.connect(self.cortar_texto)
        self.btnPegar.clicked.connect(self.pegar_texto)

    def copiar_texto(self):
        self.editorCodigo.copy()

    def cortar_texto(self):
        self.editorCodigo.cut()

    def pegar_texto(self):
        self.editorCodigo.paste()
