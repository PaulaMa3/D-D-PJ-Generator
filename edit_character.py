import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from add_character import AddCharacter


class EditCharacter(AddCharacter):
    def __init__(self, parent, main_window, character_id=None):
        super().__init__(parent, main_window)  # Pasa 'main_window' correctamente al constructor de AddCharacter
        self.character_id = character_id

        # Después de crear el frame, cargamos los datos del personaje
        if self.character_id is not None:
            self.load_character_data()

        # Permitir que el grid se ajuste a los contenidos
        self.grid_propagate(True)

    def load_character_data(self):
        # Cargar los datos del personaje desde la base de datos
        query = '''SELECT name, race_id, class_id, background_id, image_path 
                   FROM characters 
                   WHERE id = ?'''
        character_data = self.db_query(query, (self.character_id,)).fetchone()

        # Cargar los datos en los campos correspondientes
        if character_data:
            self.entry_name.insert(0, character_data[0])  # Nombre

            # Cargar la raza
            race_name = self.db_query('SELECT name FROM races WHERE id = ?', (character_data[1],)).fetchone()[0]
            self.combobox_race.set(race_name)
            self.update_race_bonuses()

            # Cargar la clase
            class_name = self.db_query('SELECT name FROM classes WHERE id = ?', (character_data[2],)).fetchone()[0]
            self.combobox_c_class.set(class_name)
            self.highlight_class_skills()

            # Cargar el trasfondo
            background_name = \
                self.db_query('SELECT name FROM backgrounds WHERE id = ?', (character_data[3],)).fetchone()[0]
            self.combobox_background.set(background_name)
            self.background_features()

            # Cargar la imagen
            if character_data[4]:
                image_path = character_data[4]
                self.select_image(image_path)  # Aquí se debería cargar la imagen desde la ruta

            # Cargar los atributos del personaje
            self.load_character_attributes()

            # Cargar las habilidades seleccionadas del personaje
            self.load_character_skills()

        # Asegurarse de que la ventana se ajuste al contenido cargado
        self.update_idletasks()

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
        query = '''SELECT s.name 
                   FROM skills s 
                   JOIN skill_character_association sc ON s.id = sc.skill_id 
                   WHERE sc.character_id = ?'''
        skills = self.db_query(query, (self.character_id,))

        for skill_name, in skills:
            if skill_name in self.skill_vars:
                self.skill_vars[skill_name]['var'].set(True)

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

        # Actualizar habilidades
        self.update_character_skills()

        messagebox.showinfo("Éxito", "Personaje actualizado con éxito")

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
