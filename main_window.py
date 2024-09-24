import tkinter as tk
from tkinter import ttk
from add_character import AddCharacter
from see_character import SeeCharacter

class MainWindow:
    db_characters = 'database/characters.db'
    db_races = 'database/races.db'
    db_classes = 'database/classes.db'
    db_skills = 'database/skills.db'

    def __init__(self, root):
        self.window = root
        self.window.title("Generador de Fichas de Personaje")
        self.window.minsize(800, 600)  # Puedes ajustar este valor según sea necesario
        self.window.resizable(1, 1)
        self.window.wm_iconbitmap('resources/icon.ico')

        # Configuración de estilos:
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#eda268', foreground='black', font=('Garamond', 13), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#da7e37')])
        style.configure('TEntry', font=('Garamond', 11), padding=3)
        style.configure('Custom.TLabelframe', background='#F4F1DE', relief="sunken")
        style.configure('Custom.TLabelframe.Label', foreground='#3D405B', background='#F4F1DE', font=('Garamond', 20, 'bold'))
        style.configure('Custom.TFrame', background='#F4F1DE', relief="flat")
        style.configure('MessageBox.TFrame', background='#F4F1DE')

        # Otros botones
        style.configure('Light.TButton', background='#CCD5AE', foreground='black', font=('Garamond', 13), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('Light.TButton', background=[('active', '#adc178')])

        style.configure('Dark.TButton', background='#E07A5F', foreground='black', font=('Garamond', 13), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('Dark.TButton', background=[('active', '#DB6848')])

        # Configurar columnas y filas en la ventana principal
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Crear un Frame contenedor con el color de fondo
        self.background_frame = tk.Frame(self.window, background='#F4F1DE')
        self.background_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Configurar columnas y filas en el background_frame para que se expandan correctamente
        self.background_frame.columnconfigure(0, weight=1)
        self.background_frame.rowconfigure(0, weight=1)

        # Creación del contenedor Frame principal utilizando ttk.LabelFrame
        self.main_frame = ttk.LabelFrame(self.window, text=" INICIO ", labelanchor='n', style='Custom.TLabelframe')
        self.main_frame.grid(row=0, column=0, columnspan=3, pady=(35, 35), padx=5, sticky=tk.NSEW)

        # Configurar columnas para que se expandan correctamente
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)

        # Botón de crear nuevo personaje, editar o ver personajes utilizando ttk.Button
        self.boton_crear = ttk.Button(self.main_frame, text='Crear personaje', command=self.show_add_character)
        self.boton_crear.grid(row=2, column=1, padx=20, pady=(30, 10), sticky=tk.W + tk.E)
        self.boton_ver = ttk.Button(self.main_frame, text='Lista de personajes', command=self.show_see_character)
        self.boton_ver.grid(row=3, column=1, padx=20, pady=(10, 30), sticky=tk.W + tk.E)
        self.boton_salir = ttk.Button(self.main_frame, text='Salir', command=self.window.quit, style= "Dark.TButton")
        self.boton_salir.grid(row=4, column=1, padx=20, pady=(10, 30), sticky=tk.W + tk.E)

        # Inicializar el Frame de AddCharacter pero no mostrarlo todavía
        self.add_character_frame = AddCharacter(self.window, self)
        self.add_character_frame.grid(row=0, column=0, columnspan=3, pady=(5, 20), padx=20, sticky=tk.W + tk.E)
        self.add_character_frame.grid_propagate(True)  # Permitir que el frame crezca según su contenido
        self.add_character_frame.grid_remove()

        # Inicializar el Frame de SeeCharacter pero no mostrarlo todavía
        self.see_character_frame = SeeCharacter(self.window, self)
        self.see_character_frame.grid(row=0, column=0, columnspan=3, pady=(5, 20), padx=20, sticky=tk.W + tk.E)
        self.see_character_frame.grid_propagate(True)  # Permitir que el frame crezca según su contenido
        self.see_character_frame.grid_remove()

        self.center_window()

    def center_window(self):
        self.window.update_idletasks()  # Asegúrate de que se actualice todo antes de centrar
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def show_add_character(self):
        self.main_frame.grid_remove()  # Ocultar el frame principal
        self.add_character_frame.grid()  # Mostrar el frame de AddCharacter

        # Establecer un tamaño fijo mayor que se ajuste a todos los elementos de AddCharacter
        self.window.geometry("1350x1000")  # Establecer el tamaño exacto de la ventana para AddCharacter

        self.center_window()  # Centrar la ventana en la pantalla

    def show_see_character(self):
        self.main_frame.grid_remove()
        self.see_character_frame.grid_remove()  # Ocultar el frame de SeeCharacter
        self.add_character_frame.grid_remove()  # Ocultar el frame de AddCharacter
        self.see_character_frame.grid()
        self.adjust_window_size()  # Ajustar el tamaño de la ventana


    def show_main_window(self):
        self.add_character_frame.grid_remove()  # Ocultar el frame de AddCharacter
        self.see_character_frame.grid_remove()  # Ocultar el frame de SeeCharacter
        self.main_frame.grid()  # Mostrar el frame principal
        self.adjust_window_size()  # Ajustar el tamaño de la ventana

    def adjust_window_size(self):
        self.window.update_idletasks()  # Actualizar el layout
        new_width = self.window.winfo_reqwidth()  # Obtener el ancho requerido
        new_height = self.window.winfo_reqheight()  # Obtener la altura requerida
        x = (self.window.winfo_screenwidth() // 2) - (new_width // 2)
        y = (self.window.winfo_screenheight() // 2) - (new_height // 2)
        self.window.geometry(f"{new_width}x{new_height}+{x}+{y}")  # Ajustar la geometría y centrar la ventana
