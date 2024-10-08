import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from add_character import AddCharacter, calculate_modifier
from db_utils import get_saving_throws


class EditCharacter(AddCharacter):
    def __init__(self, parent, main_window, character_id=None):
        super().__init__(parent, main_window)  # Pasa 'main_window' correctamente al constructor de AddCharacter
        self.character_id = character_id

        # Configurar columnas y filas en el frame principal para que se expanda correctamente
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)  # Permitir que la columna se expanda
        self.rowconfigure(0, weight=1)  # Permitir que la fila se expanda

        # Permitir que el frame de edición se ajuste a su contenido
        self.grid_propagate(True)
        self.pack_propagate(True)

        # Después de crear el frame, cargamos los datos del personaje si es necesario
        if self.character_id is not None:
            self.load_character_data()

        # Permitir que el grid se ajuste a los contenidos
        self.grid_propagate(True)
        # Sobrescribe el botón de "Volver a Inicio" para que lleve a SeeCharacter
        self.back_button.config(command=self.go_to_see_character)

    def load_character_data(self):
        # Cargar los datos del personaje desde la base de datos
        query = '''SELECT name, race_id, class_id, background_id, image_path 
                   FROM characters 
                   WHERE id = ?'''
        character_data = self.db_query(query, (self.character_id,)).fetchone()

        if character_data:
            self.entry_name.insert(0, character_data[0])  # Nombre del personaje

            # Cargar la raza
            race_name = self.db_query('SELECT name FROM races WHERE id = ?', (character_data[1],)).fetchone()[0]
            self.combobox_race.set(race_name)
            self.update_race_bonuses()

            # Cargar la clase (sin mostrar el pop-up)
            class_name = self.db_query('SELECT name FROM classes WHERE id = ?', (character_data[2],)).fetchone()[0]
            self.combobox_c_class.set(class_name)
            self.highlight_class_skills(show_popup=False)  # Llamar con show_popup=False

            # Cargar el trasfondo
            background_name = self.db_query('SELECT name FROM backgrounds WHERE id = ?', (character_data[3],)).fetchone()[0]
            self.combobox_background.set(background_name)
            self.background_features()

            # Cargar la imagen
            if character_data[4]:
                image_path = character_data[4]
                self.select_image(image_path)  # Cargar la imagen desde la ruta

            # Cargar los atributos del personaje
            self.load_character_attributes()

            # Cargar las habilidades seleccionadas del personaje
            self.load_character_skills()

            # Cargar la armadura asociada al personaje
            self.load_character_armor()

            # Actualiza la velocidad al cargar el personaje
            self.update_race_bonuses()

        # Asegurarse de que la ventana se ajuste al contenido cargado
        self.update_idletasks()

    def update_race_bonuses(self, event=None):
        selected_race = self.combobox_race.get()
        bonuses = self.race_bonuses.get(selected_race, {})

        self.strength_info.config(text=f"+{bonuses.get('Fuerza', 0)}")
        self.dexterity_info.config(text=f"+{bonuses.get('Destreza', 0)}")
        self.constitution_info.config(text=f"+{bonuses.get('Constitución', 0)}")
        self.intelligence_info.config(text=f"+{bonuses.get('Inteligencia', 0)}")
        self.wisdom_info.config(text=f"+{bonuses.get('Sabiduría', 0)}")
        self.charisma_info.config(text=f"+{bonuses.get('Carisma', 0)}")

        # Actualiza la velocidad
        self.speed_info_label.config(text=f"{bonuses.get('Velocidad', 0)}")

        self.update_languages()  # Actualizar también los idiomas

    def load_character_armor(self):
        query = '''SELECT a.name 
                   FROM armors a 
                   JOIN character_armor_association ca ON a.id = ca.armor_id 
                   WHERE ca.character_id = ?'''
        armor = self.db_query(query, (self.character_id,)).fetchone()

        if armor:
            self.combobox_equipment.set(armor[0])  # Mostrar la armadura en el combobox

    def load_character_attributes(self):
        query = '''SELECT a.name, ac.value 
                   FROM attributes a 
                   JOIN attribute_character_association ac ON a.id = ac.attribute_id 
                   WHERE ac.character_id = ?'''
        attributes = self.db_query(query, (self.character_id,))

        for attr_name, attr_value in attributes:
            if attr_name == 'Fuerza':
                self.strength_entry.insert(0, str(attr_value))
            elif attr_name == 'Destreza':
                self.dexterity_entry.insert(0, str(attr_value))
            elif attr_name == 'Constitución':
                self.constitution_entry.insert(0, str(attr_value))
            elif attr_name == 'Inteligencia':
                self.intelligence_entry.insert(0, str(attr_value))
            elif attr_name == 'Sabiduría':
                self.wisdom_entry.insert(0, str(attr_value))
            elif attr_name == 'Carisma':
                self.charisma_entry.insert(0, str(attr_value))

    def load_character_skills(self):
        # Consulta que obtiene las habilidades seleccionadas del personaje
        query = '''SELECT s.name, sc.value 
                   FROM skills s 
                   JOIN skill_character_association sc ON s.id = sc.skill_id 
                   WHERE sc.character_id = ?'''
        skills = self.db_query(query, (self.character_id,))

        # Desmarcar todas las habilidades antes de cargar las habilidades del personaje
        for skill_name in self.skill_vars:
            self.skill_vars[skill_name]['var'].set(False)

        # Marcar las habilidades del personaje basadas en el valor asociado en la tabla intermedia
        for skill_name, skill_value in skills:
            if skill_name in self.skill_vars:
                self.skill_vars[skill_name]['var'].set(True)
        self.update_saving_throws()

    def update_saving_throws(self, event=None):
        # Obtener la clase seleccionada
        selected_class = self.combobox_c_class.get()

        # Obtener las tiradas de salvación para la clase seleccionada
        saving_throws_class = get_saving_throws(selected_class)

        # Bonificador de competencia fijo (por ejemplo, nivel 1)
        proficiency_bonus = 2

        # Obtener los modificadores de los atributos
        strength_mod = calculate_modifier(int(self.strength_entry.get() or 0))
        dexterity_mod = calculate_modifier(int(self.dexterity_entry.get() or 0))
        constitution_mod = calculate_modifier(int(self.constitution_entry.get() or 0))
        intelligence_mod = calculate_modifier(int(self.intelligence_entry.get() or 0))
        wisdom_mod = calculate_modifier(int(self.wisdom_entry.get() or 0))
        charisma_mod = calculate_modifier(int(self.charisma_entry.get() or 0))

        # Diccionario para las tiradas de salvación y sus modificadores
        saving_throws = {
            "Fuerza": strength_mod,
            "Destreza": dexterity_mod,
            "Constitución": constitution_mod,
            "Inteligencia": intelligence_mod,
            "Sabiduría": wisdom_mod,
            "Carisma": charisma_mod
        }

        # Crear la cadena de texto para las tiradas de salvación
        saving_throws_text = ""
        for attribute, modifier in saving_throws.items():
            if attribute in saving_throws_class:
                saving_throws_text += f"● {attribute}: +{modifier + proficiency_bonus}\n"
            else:
                # Atributo normal sin negrita y sin bonificador
                saving_throws_text += f"○ {attribute}\n"

        # Actualizar el label con el texto generado
        self.saving_throws_info_label.config(text=saving_throws_text, font=("Garamond", 13))

    def update_character_attributes(self):
        attributes = [
            ('Fuerza', self.strength_entry.get()),
            ('Destreza', self.dexterity_entry.get()),
            ('Constitución', self.constitution_entry.get()),
            ('Inteligencia', self.intelligence_entry.get()),
            ('Sabiduría', self.wisdom_entry.get()),
            ('Carisma', self.charisma_entry.get())
        ]

        for attr_name, attr_value in attributes:
            attr_id = self.db_query('SELECT id FROM attributes WHERE name = ?', (attr_name,)).fetchone()[0]
            self.db_query('''UPDATE attribute_character_association 
                             SET value = ? 
                             WHERE character_id = ? AND attribute_id = ?''',
                          (attr_value, self.character_id, attr_id))

    def update_character_skills(self):
        self.db_query('DELETE FROM skill_character_association WHERE character_id = ?', (self.character_id,))
        for skill_name, skill_data in self.skill_vars.items():
            if skill_data['var'].get():
                skill_id = self.db_query('SELECT id FROM skills WHERE name = ?', (skill_name,)).fetchone()[0]
                self.db_query('''INSERT INTO skill_character_association (skill_id, character_id, value) 
                                 VALUES (?, ?, 1)''', (skill_id, self.character_id))

    def update_character_armor(self):
        # Eliminar la asociación existente de armadura
        self.db_query('DELETE FROM character_armor_association WHERE character_id = ?', (self.character_id,))

        # Obtener el ID de la armadura seleccionada
        selected_armor = self.combobox_equipment.get()
        armor_id = self.db_query('SELECT id FROM armors WHERE name = ?', (selected_armor,)).fetchone()

        if armor_id:
            armor_id = armor_id[0]
            # Insertar la nueva asociación
            self.db_query('INSERT INTO character_armor_association (character_id, armor_id) VALUES (?, ?)',
                          (self.character_id, armor_id))

    def save_character(self):
        if not self.validate_attributes():
            return

        # Obtener los IDs de raza, clase y trasfondo como antes
        race_id = self.db_query('SELECT id FROM races WHERE name = ?', (self.combobox_race.get(),)).fetchone()[0]
        class_id = self.db_query('SELECT id FROM classes WHERE name = ?', (self.combobox_c_class.get(),)).fetchone()[0]
        background_id = \
            self.db_query('SELECT id FROM backgrounds WHERE name = ?', (self.combobox_background.get(),)).fetchone()[0]

        # Actualizar los datos del personaje
        query = '''UPDATE characters 
                   SET name = ?, race_id = ?, class_id = ?, background_id = ?, image_path = ? 
                   WHERE id = ?'''
        parametros = (
            self.entry_name.get(),
            race_id,
            class_id,
            background_id,
            getattr(self, 'selected_image_path', None),
            self.character_id
        )
        self.db_query(query, parametros)

        # Actualizar atributos
        self.update_character_attributes()

        # Actualizar armadura
        self.update_character_armor()

        # Actualizar habilidades
        self.update_character_skills()

        messagebox.showinfo("Éxito", "Personaje actualizado con éxito")

        self.go_to_see_character()  # Aquí llamamos al método para ir a see_character

    def go_to_see_character(self):
        # Ocultar la vista de edición
        self.grid_remove()
        self.main_window.main_frame.grid_remove()  # Asegúrate de ocultar el frame principal

        # Mostrar la vista de personajes (see_character)
        self.main_window.see_character_frame.grid()  # Mostrar la vista de personajes
        self.main_window.see_character_frame.get_character()  # Refrescar la lista de personajes con los cambios        self.main_window.window.geometry("915x1000")  # Ajustar el tamaño de la ventana si es necesario
        self.main_window.window.geometry("915x1000")
        self.main_window.center_window()  # Centrar la ventana


