from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from db import session
from main_window import MainWindow
from models import User
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())


def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()


def register_user(username, password, email):
    if get_user_by_username(username):
        return "Error: El nombre de usuario ya existe."
    try:
        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password, email=email)
        session.add(new_user)
        session.commit()
        return "Registro completado con éxito."
    except Exception as e:
        return f"Error: {str(e)}"


def validate_registration(username, password, email):
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    if '@' not in email or '.' not in email:
        return False, "El correo electrónico no es válido."
    return True, None


def login(username, password):
    user = get_user_by_username(username)
    if user:
        if check_password(user.password, password):
            return True
        else:
            return "Error: Contraseña incorrecta."
    else:
        return "Error: Usuario no encontrado."


class AuthWindow(ttk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        # Configuración de estilos para que coincida con la ventana principal
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#eda268', foreground='black', font=('Garamond', 13), borderwidth=1,
                        focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#da7e37')])
        style.configure('TEntry', font=('Garamond', 11), padding=3)
        style.configure('Custom.TLabelframe', background='#F4F1DE', relief="sunken")
        style.configure('Custom.TLabelframe.Label', foreground='#3D405B', background='#F4F1DE',
                        font=('Garamond', 20, 'bold'))
        style.configure('Custom.TFrame', background='#F4F1DE', relief="flat")
        style.configure('MessageBox.TFrame', background='#F4F1DE')

        style.configure('Light.TButton', background='#CCD5AE', foreground='black', font=('Garamond', 13), borderwidth=1,
                        focusthickness=3, focuscolor='none')
        style.map('Light.TButton', background=[('active', '#adc178')])
        style.configure('Dark.TButton', background='#E07A5F', foreground='black', font=('Garamond', 13), borderwidth=1,
                        focusthickness=3, focuscolor='none')
        style.map('Dark.TButton', background=[('active', '#DB6848')])

        # Crear el frame de fondo con el mismo color que en la ventana principal
        self.background_frame = tk.Frame(self, background='#F4F1DE')
        self.background_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.create_login_widgets()

    def create_login_widgets(self):
        # Configurar un frame central que contenga todos los widgets
        central_frame = ttk.LabelFrame(self.background_frame, text="Inicio de Sesión", labelanchor="n",
                                       style='Custom.TLabelframe')
        central_frame.grid(row=0, column=0, columnspan=10, pady=50, padx=50, sticky=tk.NSEW)
        central_frame.columnconfigure(1, weight=1)
        central_frame.rowconfigure(0, weight=1)

        # Campo de nombre de usuario
        self.label_username = ttk.Label(central_frame, text="Nombre de usuario:", font=("Garamond", 16),
                                        background='#F4F1DE')
        self.label_username.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_username = ttk.Entry(central_frame)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        # Campo de contraseña
        self.label_password = ttk.Label(central_frame, text="Contraseña:", font=("Garamond", 16), background='#F4F1DE')
        self.label_password.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_password = ttk.Entry(central_frame, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        # Botón de inicio de sesión
        self.button_login = ttk.Button(central_frame, text="Iniciar sesión", command=self.attempt_login,
                                       style='Light.TButton')
        self.button_login.grid(row=3, column=1, padx=10, pady=10)

        # Botón para ir a la pantalla de registro
        self.button_register = ttk.Button(central_frame, text="Registrarse", command=self.show_register_widgets,
                                          style='Light.TButton')
        self.button_register.grid(row=4, column=1, padx=10, pady=10)

    def create_register_widgets(self):
        # Crear un nuevo frame para el registro
        central_frame = ttk.LabelFrame(self.background_frame, text="Registrar Nuevo Usuario", style='Custom.TLabelframe')
        central_frame.grid(row=0, column=0, columnspan=10, pady=50, padx=50, sticky=tk.NSEW)
        central_frame.columnconfigure(1, weight=1)
        central_frame.rowconfigure(0, weight=1)

        # Título de la ventana de registro
        self.label_title = ttk.Label(central_frame, text="Registrar Nuevo Usuario", style='Custom.TLabelframe')
        self.label_title.grid(row=0, column=1, pady=10)

        # Campo de nombre de usuario
        self.label_username = ttk.Label(central_frame, text="Nombre de usuario:", font=("Garamond", 16),
                                        background='#F4F1DE')
        self.label_username.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_username = ttk.Entry(central_frame)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        # Campo de correo electrónico
        self.label_email = ttk.Label(central_frame, text="Correo electrónico:", font=("Garamond", 16),
                                     background='#F4F1DE')
        self.label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_email = ttk.Entry(central_frame)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10)

        # Campo de contraseña
        self.label_password = ttk.Label(central_frame, text="Contraseña:", font=("Garamond", 16), background='#F4F1DE')
        self.label_password.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_password = ttk.Entry(central_frame, show="*")
        self.entry_password.grid(row=3, column=1, padx=10, pady=10)

        # Botón de registro
        self.button_register = ttk.Button(central_frame, text="Registrar", command=self.attempt_register,
                                          style='Light.TButton')
        self.button_register.grid(row=4, column=1, padx=10, pady=10)

        # Botón para volver a la pantalla de inicio de sesión
        self.button_back = ttk.Button(central_frame, text="Volver", command=self.show_login_widgets,
                                      style='Dark.TButton')
        self.button_back.grid(row=5, column=1, padx=10, pady=10)

    def attempt_login(self):
        # Implementación de la lógica de inicio de sesión
        username = self.entry_username.get()
        password = self.entry_password.get()

        result = login(username, password)
        if result is True:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.main_window = MainWindow(self.master, username)
            self.main_window.show_main_window()
            self.grid_forget()  # Ocultar la ventana de login
        else:
            messagebox.showerror("Error", result)

    def attempt_register(self):
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        valid, message = validate_registration(username, password, email)
        if not valid:
            messagebox.showerror("Error", message)
            return

        result = register_user(username, password, email)
        if "Error" in result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Éxito", result)
            self.show_login_widgets()  # Volver a la pantalla de inicio de sesión tras registrarse

    def show_register_widgets(self):
        self.clear_widgets()
        self.create_register_widgets()

    def show_login_widgets(self):
        self.clear_widgets()
        self.create_login_widgets()

    def clear_widgets(self):
        for widget in self.background_frame.winfo_children():
            widget.grid_remove()
