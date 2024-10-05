import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from edit_character import EditCharacter


class SeeCharacter(ttk.Frame):
    db_characters = 'database/characters.db'
    db_races = 'database/races.db'
    db_classes = 'database/classes.db'
    db_skills = 'database/skills.db'

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.parent = parent
        self.main_window = main_window

        # Crear un Frame contenedor con el color de fondo
        background_frame = tk.Frame(self, background='#F4F1DE')
        background_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Configurar columnas y filas en el background_frame para que se expandan correctamente
        background_frame.columnconfigure(2, weight=1)
        background_frame.rowconfigure(0, weight=1)

        # Configurar un frame central que contenga todos los widgets
        self.central_frame = ttk.Frame(self, style='Custom.TLabelframe')
        self.central_frame.grid(row=0, column=0, columnspan=10, padx=0, pady=0, sticky="nsew")
        self.central_frame.columnconfigure(0, weight=1)
        self.central_frame.rowconfigure(2, weight=1)

        message_box = ttk.Frame(self.central_frame, style='Custom.TLabelframe')
        message_box.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="ew", columnspan=3)

        self.ok_message = ttk.Label(message_box, text="", font=("Garamond", 14),
                                    foreground='green', background='#F4F1DE')
        self.ok_message.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.error_message = ttk.Label(message_box, text="", font=("Garamond", 14),
                                       foreground='red', background='#F4F1DE')
        self.error_message.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Añadir barra de búsqueda
        self.search_entry = ttk.Entry(self.central_frame, font=('Garamond', 15))
        self.search_entry.grid(row=2, column=0, padx=10, pady=0, sticky=tk.W + tk.E, columnspan=2)

        # Crear un frame para los botones
        button_frame = ttk.Frame(self.central_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=2, padx=5, pady=(0, 5), sticky="ne")

        self.search_button = ttk.Button(button_frame, text="Buscar", command=self.search_character,
                                        style='Light.TButton')
        self.search_button.grid(row=0, column=0, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar", command=self.del_character, style='Dark.TButton')
        self.delete_button.grid(row=0, column=1, padx=5)

        self.back_button = ttk.Button(button_frame, text="Volver", command=self.main_window.show_main_window,
                                      style='TButton')
        self.back_button.grid(row=0, column=2, padx=5)

        self.show_all_button = ttk.Button(button_frame, text="Mostrar todos", command=self.get_character,
                                          style='Light.TButton')
        self.show_all_button.grid(row=0, column=3, padx=5)

        # Inicializar la tabla donde se mostrarán los resultados
        self.tabla = ttk.Treeview(self.central_frame, columns=(
            "Name", "Race", "Class", "Background", "Strength", "Dexterity", "Constitution", "Intelligence",
            "Wisdom", "Charisma", "Speed"), show='headings')

        self.tabla.heading("Name", text="Nombre")
        self.tabla.heading("Race", text="Raza")
        self.tabla.heading("Class", text="Clase")
        self.tabla.heading("Background", text="Trasfondo")
        self.tabla.heading("Strength", text="Fuerza")
        self.tabla.heading("Dexterity", text="Destreza")
        self.tabla.heading("Constitution", text="Constitución")
        self.tabla.heading("Intelligence", text="Inteligencia")
        self.tabla.heading("Wisdom", text="Sabiduría")
        self.tabla.heading("Charisma", text="Carisma")
        self.tabla.heading("Speed", text="Velocidad")

        # Establecer el ancho de las columnas
        self.tabla.column("Name", width=100)
        self.tabla.column("Race", width=100)
        self.tabla.column("Class", width=100)
        self.tabla.column("Background", width=100)
        self.tabla.column("Strength", width=60)
        self.tabla.column("Dexterity", width=60)
        self.tabla.column("Constitution", width=80)
        self.tabla.column("Intelligence", width=80)
        self.tabla.column("Wisdom", width=60)
        self.tabla.column("Charisma", width=60)
        self.tabla.column("Speed", width=70)

        self.tabla.grid(row=3, column=0, columnspan=3, padx=0, pady=0, sticky=tk.NSEW)
        self.get_character()
        # En el método __init__
        self.tabla.bind("<<TreeviewSelect>>", self.show_character_info)

        # Configurar expansión de la tabla
        self.central_frame.columnconfigure(0, weight=1)
        self.central_frame.rowconfigure(2, weight=1)

        # Crear un frame debajo de la tabla para mostrar la información del personaje seleccionado
        self.info_frame = ttk.Frame(self.central_frame, style='Custom.TFrame')
        self.info_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=1)

        self.data_frame = ttk.Frame(self.info_frame, style='Custom.TFrame')
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Añadir un canvas para la imagen
        self.canvas = tk.Canvas(self.data_frame, width=150, height=150)
        self.canvas.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nw")

        # Añadir labels para mostrar el nombre y otros detalles
        self.label_name = ttk.Label(self.data_frame, text="", font=("Garamond", 16), style='Custom.TLabelframe.Label')
        self.label_name.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.edit_character_button = ttk.Button(self.data_frame, text="Editar Personaje",
                                                command=self.show_edit_character, style='TButton')
        self.edit_character_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew" )

        # Frame para la gráfica
        self.chart_frame = ttk.Frame(self.info_frame)
        self.chart_frame.grid(row=0, column=1, padx=(0, 20), pady=(15, 5), sticky="nsew")

        # Asegurarse de que el frame se expanda
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.rowconfigure(1, weight=1)


        # Inicializar el Frame de SeeCharacter pero no mostrarlo todavía
        self.edit_character_frame = EditCharacter(self.parent, self.main_window)
        self.edit_character_frame.grid(row=0, column=0, columnspan=3, pady=(5, 20), padx=20, sticky=tk.W + tk.E)
        self.edit_character_frame.grid_propagate(True)  # Permitir que el frame crezca según su contenido
        self.edit_character_frame.grid_remove()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_characters) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return cursor.fetchall()  # Asegúrate de devolver todos los resultados

    def get_character(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = '''SELECT DISTINCT characters.name, 
                            characters.image_path, 
                            races.name AS race_name, 
                            classes.name AS class_name,  
                            backgrounds.name AS background_name,
                            COALESCE(attr_str.value, 0) AS strength, 
                            COALESCE(attr_dex.value, 0) AS dexterity, 
                            COALESCE(attr_con.value, 0) AS constitution, 
                            COALESCE(attr_int.value, 0) AS intelligence, 
                            COALESCE(attr_wis.value, 0) AS wisdom, 
                            COALESCE(attr_cha.value, 0) AS charisma, 
                            races.speed AS speed
               FROM characters
               LEFT JOIN races ON characters.race_id = races.id  
               LEFT JOIN classes ON characters.class_id = classes.id
               LEFT JOIN backgrounds ON characters.background_id = backgrounds.id
               LEFT JOIN attribute_character_association AS attr_str               
                  ON characters.id = attr_str.character_id AND attr_str.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Fuerza')
               LEFT JOIN attribute_character_association AS attr_dex 
                  ON characters.id = attr_dex.character_id AND attr_dex.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Destreza')
               LEFT JOIN attribute_character_association AS attr_con 
                  ON characters.id = attr_con.character_id AND attr_con.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Constitución')
               LEFT JOIN attribute_character_association AS attr_int 
                  ON characters.id = attr_int.character_id AND attr_int.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Inteligencia')
               LEFT JOIN attribute_character_association AS attr_wis 
                  ON characters.id = attr_wis.character_id AND attr_wis.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Sabiduría')
               LEFT JOIN attribute_character_association AS attr_cha 
                  ON characters.id = attr_cha.character_id AND attr_cha.attribute_id = 
                     (SELECT id FROM attributes WHERE name = 'Carisma')
               ORDER BY characters.name DESC'''

        registros_db = self.db_consulta(query)

        for fila in registros_db:
            self.tabla.insert('', 'end', values=(
                fila[0],  # Nombre
                fila[2],  # Raza
                fila[3],  # Clase
                fila[4],  # Trasfondo
                fila[5],  # Fuerza
                fila[6],  # Destreza
                fila[7],  # Constitución
                fila[8],  # Inteligencia
                fila[9],  # Sabiduría
                fila[10],  # Carisma
                fila[11]  # Velocidad
            ))

    def show_character_info(self, event):
        self.edit_character_button = ttk.Button(self.data_frame, text="Editar Personaje",
                                                command=self.show_edit_character, style='TButton')
        self.edit_character_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")


        selected_items = self.tabla.selection()

        selected_item = selected_items[0]

        character_data = self.tabla.item(selected_item)['values']

        name = character_data[0]
        race = character_data[1]
        class_ = character_data[2]
        background = character_data[3]
        strength = character_data[4]
        dexterity = character_data[5]
        constitution = character_data[6]
        intelligence = character_data[7]
        wisdom = character_data[8]
        charisma = character_data[9]
        speed = character_data[10]

        # Mostrar el nombre del personaje
        self.label_name.config(text=f"Nombre: {name}\nRaza: {race}\nClase: {class_}\nTrasfondo: {background}")

        # Recoge la ruta de la imagen desde el conjunto de datos original
        image_path = self.db_consulta('SELECT image_path FROM characters WHERE name = ?', (name,))[0][0]

        # Mostrar la imagen si existe
        if isinstance(image_path, str) and image_path.endswith(('.png', '.jpg', '.jpeg')):
            try:
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor="nw", image=photo)
                self.canvas.image = photo  # Mantener referencia
            except FileNotFoundError:
                self.canvas.delete("all")
                self.canvas.create_text(75, 75, text="Sin Imagen", anchor="center")
        else:
            self.canvas.delete("all")
            self.canvas.create_text(75, 75, text="Sin Imagen", anchor="center")

        # Mostrar gráfica de atributos
        self.show_attribute_chart([strength, dexterity, constitution, intelligence, wisdom, charisma])

    def show_attribute_chart(self, attributes):
        # Limpiar cualquier gráfica anterior antes de crear una nueva
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Nombres de los atributos
        labels = ['Fuerza', 'Destreza', 'Constitución', 'Inteligencia', 'Sabiduría', 'Carisma']

        # Número de variables
        num_vars = len(labels)

        # Ángulo de cada eje del gráfico de radar
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Completar el ciclo para cerrar el gráfico
        attributes += attributes[:1]
        angles += angles[:1]

        # Iniciar el gráfico de radar con un tamaño ajustado
        fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))

        # Dibujar la línea del gráfico con un tono verde suave
        ax.plot(angles, attributes, color='#A7C957', linewidth=2)

        # Rellenar el gráfico con un verde transparente
        ax.fill(angles, attributes, color=(167/255, 201/255, 87/255, 0.4), alpha=0.4)

        # Ajustar el color de los ejes y las etiquetas a un marrón suave
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='#6C584C')

        # Ajustar el color del borde y las líneas de la gráfica
        ax.spines['polar'].set_color('#6C584C')
        ax.spines['polar'].set_linewidth(1)

        # Ajustar el layout para que encaje mejor en el frame
        fig.tight_layout()

        # Mostrar la gráfica en el frame de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Forzar la actualización del tamaño de la ventana para ajustarse al contenido
        self.master.update_idletasks()

    def search_character(self):
        self.error_message['text'] = ''

        search_term = self.search_entry.get()
        if search_term:  # Si hay un término de búsqueda
            query = '''SELECT characters.name, races.name AS race_name, classes.name AS class_name, backgrounds.name AS background_name, 
                        COALESCE(attr_str.value, 0) AS strength, COALESCE(attr_dex.value, 0) AS dexterity, COALESCE(attr_con.value, 0) AS constitution, 
                        COALESCE(attr_int.value, 0) AS intelligence, COALESCE(attr_wis.value, 0) AS wisdom, COALESCE(attr_cha.value, 0) AS charisma, 
                        races.speed AS speed
                        FROM characters
                        LEFT JOIN races ON characters.race_id = races.id
                        LEFT JOIN classes ON characters.class_id = classes.id
                        LEFT JOIN backgrounds ON characters.background_id = backgrounds.id  
                        LEFT JOIN attribute_character_association AS attr_str ON characters.id = attr_str.character_id AND attr_str.attribute_id = (SELECT id FROM attributes WHERE name = 'Fuerza')
                        LEFT JOIN attribute_character_association AS attr_dex ON characters.id = attr_dex.character_id AND attr_dex.attribute_id = (SELECT id FROM attributes WHERE name = 'Destreza')
                        LEFT JOIN attribute_character_association AS attr_con ON characters.id = attr_con.character_id AND attr_con.attribute_id = (SELECT id FROM attributes WHERE name = 'Constitución')
                        LEFT JOIN attribute_character_association AS attr_int ON characters.id = attr_int.character_id AND attr_int.attribute_id = (SELECT id FROM attributes WHERE name = 'Inteligencia')
                        LEFT JOIN attribute_character_association AS attr_wis ON characters.id = attr_wis.character_id AND attr_wis.attribute_id = (SELECT id FROM attributes WHERE name = 'Sabiduría')
                        LEFT JOIN attribute_character_association AS attr_cha ON characters.id = attr_cha.character_id AND attr_cha.attribute_id = (SELECT id FROM attributes WHERE name = 'Carisma')
                        WHERE characters.name LIKE ?
                        ORDER BY characters.name DESC'''
            registros_db = self.db_consulta(query, ('%' + search_term + '%',))
        else:
            query = '''SELECT characters.name, races.name AS race_name, classes.name AS class_name, backgrounds.name AS background_name, 
                        COALESCE(attr_str.value, 0) AS strength, COALESCE(attr_dex.value, 0) AS dexterity, COALESCE(attr_con.value, 0) AS constitution, 
                        COALESCE(attr_int.value, 0) AS intelligence, COALESCE(attr_wis.value, 0) AS wisdom, COALESCE(attr_cha.value, 0) AS charisma, 
                        races.speed AS speed
                        FROM characters
                        LEFT JOIN races ON characters.race_id = races.id
                        LEFT JOIN classes ON characters.class_id = classes.id
                        LEFT JOIN backgrounds ON characters.background_id = backgrounds.id
                        LEFT JOIN attribute_character_association AS attr_str ON characters.id = attr_str.character_id AND attr_str.attribute_id = (SELECT id FROM attributes WHERE name = 'Fuerza')
                        LEFT JOIN attribute_character_association AS attr_dex ON characters.id = attr_dex.character_id AND attr_dex.attribute_id = (SELECT id FROM attributes WHERE name = 'Destreza')
                        LEFT JOIN attribute_character_association AS attr_con ON characters.id = attr_con.character_id AND attr_con.attribute_id = (SELECT id FROM attributes WHERE name = 'Constitución')
                        LEFT JOIN attribute_character_association AS attr_int ON characters.id = attr_int.character_id AND attr_int.attribute_id = (SELECT id FROM attributes WHERE name = 'Inteligencia')
                        LEFT JOIN attribute_character_association AS attr_wis ON characters.id = attr_wis.character_id AND attr_wis.attribute_id = (SELECT id FROM attributes WHERE name = 'Sabiduría')
                        LEFT JOIN attribute_character_association AS attr_cha ON characters.id = attr_cha.character_id AND attr_cha.attribute_id = (SELECT id FROM attributes WHERE name = 'Carisma')
                        ORDER BY characters.name DESC'''
            registros_db = self.db_consulta(query)

        # Limpiar la tabla actual y mostrar los resultados de la búsqueda
        self.tabla.delete(*self.tabla.get_children())
        for fila in registros_db:
            self.tabla.insert('', 'end', values=(
                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10]
            ))

    def del_character(self):
        try:
            selected_item = self.tabla.selection()[0]
        except IndexError:
            self.error_message['text'] = 'Por favor, seleccione un personaje'
            return

        nombre = self.tabla.item(selected_item)['values'][0]
        query = 'DELETE FROM characters WHERE name = ?'
        self.db_consulta(query, (nombre,))
        self.ok_message['text'] = f'Personaje {nombre} eliminado con éxito'
        self.get_character()

    def show_edit_character(self):
        selected_items = self.tabla.selection()
        if not selected_items:
            messagebox.showerror("Error", "Por favor selecciona un personaje para editar.")
            return

        selected_item = selected_items[0]
        character_id = self.tabla.item(selected_item)['values'][
            0]  # Asume que la primera columna tiene el ID del personaje

        # Crea una nueva instancia del frame de edición y pásale el ID del personaje seleccionado
        self.edit_character_frame = EditCharacter(self.parent, self.main_window,
                                                  character_id)  # Asegúrate de pasar 'main_window'
        self.edit_character_frame.grid()  # Muestra el frame de edición
