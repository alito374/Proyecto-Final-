"""Punto de entrada de NovaCode IDE."""
from pathlib import Path
print("INICIANDO MAIN DESDE:", Path(__file__).resolve())
from editor import main

if __name__ == "__main__":
    main()
