from ttkthemes import ThemedTk
from main_window import MainWindow
from db import init_db
from resources.populate_db import populate_db
from auth_window import AuthWindow  # Importamos la ventana de autenticación
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

def main():
    init_db()
    populate_db()
    root = ThemedTk(theme="yaru")
    root.title("Generador de Fichas de Personaje")

    auth_window = AuthWindow(parent=root, main_window=None)

    auth_window.pack(expand=True, fill="both")  # Mostrar el frame de autenticación

    root.mainloop()

if __name__ == '__main__':
    main()
