
import sys

from PyQt6.QtWidgets import QApplication
from interfaz.ventana import VentanaALMA


def main():
    app = QApplication(sys.argv)

    ventana = VentanaALMA()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
