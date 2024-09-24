from ttkthemes import ThemedTk
from main_window import MainWindow
from db import init_db
from resources.populate_db import populate_db



def main():
    init_db()
    populate_db()
    root = ThemedTk(theme="yaru")
    root.title("Generador de Fichas de Personaje")
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()