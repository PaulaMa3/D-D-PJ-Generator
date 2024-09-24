import tkinter as tk
from tkinter import ttk
import sqlite3


class SeeCharacter(ttk.Frame):
    db_characters = 'database/characters.db'
    db_races = 'database/races.db'
    db_classes = 'database/classes.db'
    db_skills = 'database/skills.db'

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.parent = parent
        self.main_window = main_window

        # Configurar un frame central que contenga todos los widgets
        self.central_frame = ttk.Frame(self, style='Custom.TFrame')
        self.central_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.central_frame.columnconfigure(0, weight=1)
        self.central_frame.rowconfigure(2, weight=1)

        message_box = ttk.Frame(self.central_frame, style='Custom.TLabelframe')
        message_box.grid(row=0, column=0, padx=0, sticky="ew", columnspan=3)

        self.ok_message = ttk.Label(message_box, text="", font=("Garamond", 15),
                                    foreground='green', background='#FEFAE0')
        self.ok_message.grid(row=0, column=0, sticky="ew")

        self.error_message = ttk.Label(message_box, text="", font=("Garamond", 15),
                                       foreground='red', background='#FEFAE0')
        self.error_message.grid(row=1, column=0, sticky="ew")

        # Añadir barra de búsqueda
        self.search_entry = ttk.Entry(self.central_frame, font=('Garamond', 15))
        self.search_entry.grid(row=1, column=0, padx=10, pady=0, sticky=tk.W + tk.E, columnspan=2)

        # Crear un frame para los botones
        button_frame = ttk.Frame(self.central_frame, style='Custom.TFrame')
        button_frame.grid(row=1, column=2, padx=5, pady=(0, 5), sticky="ne")

        self.search_button = ttk.Button(button_frame, text="Buscar", command=self.search_character, style='TButton')
        self.search_button.grid(row=0, column=0, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar", command=self.del_character, style='Dark.TButton')
        self.delete_button.grid(row=0, column=1, padx=5)

        self.back_button = ttk.Button(button_frame, text="Volver", command=self.main_window.show_main_window,
                                      style='Light.TButton')
        self.back_button.grid(row=0, column=2, padx=5)

        # Inicializar la tabla donde se mostrarán los resultados
        self.tabla = ttk.Treeview(self.central_frame, columns=(
        "Name", "Race", "Class", "Level", "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma",
        "Speed"), show='headings')
        self.tabla.heading("Name", text="Nombre")
        self.tabla.heading("Race", text="Raza")
        self.tabla.heading("Class", text="Clase")
        self.tabla.heading("Level", text="Nivel")
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
        self.tabla.column("Level", width=60)
        self.tabla.column("Strength", width=60)
        self.tabla.column("Dexterity", width=60)
        self.tabla.column("Constitution", width=80)
        self.tabla.column("Intelligence", width=80)
        self.tabla.column("Wisdom", width=60)
        self.tabla.column("Charisma", width=60)
        self.tabla.column("Speed", width=60)

        self.tabla.grid(row=2, column=0, columnspan=3, padx=0, pady=0, sticky=tk.NSEW)
        self.get_character()

        # Configurar expansión de la tabla
        self.central_frame.columnconfigure(0, weight=1)
        self.central_frame.rowconfigure(2, weight=1)

    def get_character(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = '''SELECT DISTINCT characters.name, races.name AS race_name, classes.name AS class_name, characters.level, 
                    COALESCE(attr_str.value, 0) AS strength, COALESCE(attr_dex.value, 0) AS dexterity, 
                    COALESCE(attr_con.value, 0) AS constitution, 
                    COALESCE(attr_int.value, 0) AS intelligence, COALESCE(attr_wis.value, 0) AS wisdom, COALESCE(attr_cha.value, 0) AS charisma, 
                    races.speed AS speed
                    FROM characters
                    LEFT JOIN races ON characters.race_id = races.id
                    LEFT JOIN classes ON characters.class_id = classes.id
                    LEFT JOIN attribute_character_association AS attr_str ON characters.id = attr_str.character_id AND attr_str.attribute_id = (SELECT id FROM attributes WHERE name = 'Fuerza')
                    LEFT JOIN attribute_character_association AS attr_dex ON characters.id = attr_dex.character_id AND attr_dex.attribute_id = (SELECT id FROM attributes WHERE name = 'Destreza')
                    LEFT JOIN attribute_character_association AS attr_con ON characters.id = attr_con.character_id AND attr_con.attribute_id = (SELECT id FROM attributes WHERE name = 'Constitución')
                    LEFT JOIN attribute_character_association AS attr_int ON characters.id = attr_int.character_id AND attr_int.attribute_id = (SELECT id FROM attributes WHERE name = 'Inteligencia')
                    LEFT JOIN attribute_character_association AS attr_wis ON characters.id = attr_wis.character_id AND attr_wis.attribute_id = (SELECT id FROM attributes WHERE name = 'Sabiduría')
                    LEFT JOIN attribute_character_association AS attr_cha ON characters.id = attr_cha.character_id AND attr_cha.attribute_id = (SELECT id FROM attributes WHERE name = 'Carisma')
                    ORDER BY characters.name DESC
                    '''

        registros_db = self.db_consulta(query)

        for fila in registros_db:
            print(fila)  # Agrega esto para ver el contenido de cada fila
            self.tabla.insert('', 'end', values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9]))

    def search_character(self):
        search_term = self.search_entry.get()
        query = '''SELECT characters.name, races.name AS race_name, classes.name AS class_name, characters.level, 
                COALESCE(attr_str.value, 0) AS strength, COALESCE(attr_dex.value, 0) AS dexterity, COALESCE(attr_con.value, 0) AS constitution, 
                COALESCE(attr_int.value, 0) AS intelligence, COALESCE(attr_wis.value, 0) AS wisdom, COALESCE(attr_cha.value, 0) AS charisma, 
                races.speed AS speed
                FROM characters
                LEFT JOIN races ON characters.race_id = races.id
                LEFT JOIN classes ON characters.class_id = classes.id
                LEFT JOIN attribute_character_association AS attr_str ON characters.id = attr_str.character_id AND attr_str.attribute_id = (SELECT id FROM attributes WHERE name = 'Fuerza')
                LEFT JOIN attribute_character_association AS attr_dex ON characters.id = attr_dex.character_id AND attr_dex.attribute_id = (SELECT id FROM attributes WHERE name = 'Destreza')
                LEFT JOIN attribute_character_association AS attr_con ON characters.id = attr_con.character_id AND attr_con.attribute_id = (SELECT id FROM attributes WHERE name = 'Constitución')
                LEFT JOIN attribute_character_association AS attr_int ON characters.id = attr_int.character_id AND attr_int.attribute_id = (SELECT id FROM attributes WHERE name = 'Inteligencia')
                LEFT JOIN attribute_character_association AS attr_wis ON characters.id = attr_wis.character_id AND attr_wis.attribute_id = (SELECT id FROM attributes WHERE name = 'Sabiduría')
                LEFT JOIN attribute_character_association AS attr_cha ON characters.id = attr_cha.character_id AND attr_cha.attribute_id = (SELECT id FROM attributes WHERE name = 'Carisma')
                WHERE characters.name LIKE ?
                ORDER BY characters.name DESC'''

        registros_db = self.db_consulta(query, ('%' + search_term + '%',))

        # Limpiar la tabla actual y mostrar los resultados de la búsqueda
        self.tabla.delete(*self.tabla.get_children())
        for fila in registros_db:
            self.tabla.insert('', 'end', values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9]))

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_characters) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return cursor.fetchall()  # Asegúrate de devolver todos los resultados

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
