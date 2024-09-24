import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ui_elements import create_taped_label
from db_utils import *

import requests
from io import BytesIO
from PIL import Image, ImageTk


def calculate_modifier(attribute_score):
    if attribute_score <= 11:
        return 0
    elif attribute_score <= 13:
        return 1
    elif attribute_score <= 15:
        return 2
    elif attribute_score <= 17:
        return 3
    elif attribute_score <= 19:
        return 4
    else:
        return 5


class AddCharacter(ttk.Frame):
    db_characters = 'database/characters.db'

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.parent = parent
        self.main_window = main_window

        # Crear un Frame contenedor con el color de fondo
        background_frame = tk.Frame(self, background='#F4F1DE')
        background_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Configurar columnas y filas en el background_frame para que se expandan correctamente
        background_frame.columnconfigure(0, weight=1)
        background_frame.rowconfigure(0, weight=1)

        # Configurar un frame central que contenga todos los widgets
        central_frame = ttk.Frame(self, style='Custom.TFrame')
        central_frame.grid(row=0, column=0, columnspan=10, pady=0, padx=0, sticky=tk.NSEW)
        central_frame.columnconfigure(8, weight=1)
        central_frame.rowconfigure(0, weight=1)

        barra = ttk.Frame(central_frame, style='Custom.TFrame')
        barra.grid(row=1, column=0, columnspan=2, pady=(20, 5), padx=0, sticky="nsew")

        # Añadir botón Guardar
        self.save_button = ttk.Button(barra, text="Guardar", command=self.save_character)
        self.save_button.pack(side="left", padx=(35, 10))

        # Añadir botón Volver a Inicio
        self.back_button = ttk.Button(barra, text="Volver a Inicio", command=self.main_window.show_main_window, style="Dark.TButton")
        self.back_button.pack(side="left", padx=(10, 0))

        frame_ep = ttk.LabelFrame(central_frame, text="Generador de fichas de personaje", labelanchor='n', style='Custom.TLabelframe')
        frame_ep.grid(row=2, column=0, columnspan=10, pady=0, padx=(10, 10), sticky=tk.NSEW)

        # Crear un marco para la imagen y el botón
        self.image_frame = tk.Frame(frame_ep, width=150, height=150, bg="gray")
        self.image_frame.grid(row=2, column=0, rowspan=4, padx=15, pady=15, sticky="nw")
        self.image_frame.grid_propagate(False)  # Evitar que el frame se expanda o contraiga según el contenido

        self.add_image_button = ttk.Button(self.image_frame, text="Agregar Imagen", style='Light.TButton',
                                           command=self.select_image)
        self.add_image_button.place(relx=0.5, rely=0.5, anchor="center")
        self.image_frame.grid_propagate(False)  # Evitar que el frame se expanda o contraiga según el contenido

        self.label_name = ttk.Label(frame_ep, text="Nombre:", font=("Garamond", 16), background='#F4F1DE')
        self.label_name.grid(row=2, column=1, padx=(25, 5), pady=(25,5), sticky=tk.NSEW)
        self.entry_name = ttk.Entry(frame_ep, font=("Garamond", 16))
        self.entry_name.grid(row=2, column=2, padx=(5, 20), pady=(25,5), sticky=tk.NSEW)

        self.label_race = ttk.Label(frame_ep, text="Raza:", font=("Garamond", 16), background='#F4F1DE')
        self.label_race.grid(row=3, column=1, padx=(25, 5), pady=5, sticky=tk.NSEW)

        # Obtener detalles de las razas
        self.race_bonuses = get_races()

        self.combobox_race = ttk.Combobox(frame_ep, values=list(self.race_bonuses.keys()), font=('Garamond', 15),
                                          state='readonly')
        self.combobox_race.grid(row=3, column=2, padx=(5, 20), pady=5, sticky=tk.NSEW)

        # Configurar combobox_race con el comando para actualizar bonificaciones
        self.combobox_race.bind("<<ComboboxSelected>>", self.update_race_bonuses)

        self.label_class = ttk.Label(frame_ep, text="Clase:", font=("Garamond", 16), background='#F4F1DE')
        self.label_class.grid(row=4, column=1, padx=(25, 5), pady=5, sticky=tk.NSEW)
        self.combobox_c_class = ttk.Combobox(frame_ep, values=list(get_classes().keys()), font=('Garamond', 15),
                                             state='readonly')
        self.combobox_c_class.grid(row=4, column=2, padx=(5, 20), pady=5, sticky=tk.NSEW)
        self.combobox_c_class.bind("<<ComboboxSelected>>", self.update_inventory)

        self.label_level = ttk.Label(frame_ep, text="Nivel:", font=("Garamond", 16), background='#F4F1DE')
        self.label_level.grid(row=5, column=1, padx=(25, 5), pady=(5, 25), sticky=tk.NSEW)
        self.entry_level = ttk.Label(frame_ep, text="1", font=("Garamond", 16), background='#F4F1DE')
        self.entry_level.grid(row=5, column=2, padx=(5, 20), pady=(5, 25), sticky=tk.NSEW)

        self.label_proficiency_bonus = ttk.Label(frame_ep, text="Bonificador de competencia:", font=("Garamond", 16), background='#F4F1DE')
        self.label_proficiency_bonus.grid(row=2, column=4, padx=(25, 5), pady=(25,5), sticky=tk.NSEW)
        self.label_proficiency_bonus_info = ttk.Label(frame_ep, text="+2",  font=("Garamond", 15), background='#F4F1DE')
        self.label_proficiency_bonus_info.grid(row=2, column=5, padx=(5, 20), pady=(25,5), sticky=tk.NSEW)

        self.speed_label = ttk.Label(frame_ep, text="Velocidad:", font=("Garamond", 16), background='#F4F1DE')
        self.speed_label.grid(row=3, column=4, padx=(25, 5), pady=5, sticky=tk.NSEW)
        self.speed_info_label = ttk.Label(frame_ep, text="", font=("Garamond", 14), background='#F4F1DE')
        self.speed_info_label.grid(row=3, column=5, padx=(5, 20), pady=5, sticky=tk.NSEW)

        self.combobox_c_class.bind("<<ComboboxSelected>>", self.highlight_class_skills)

        self.armor_class_label = ttk.Label(frame_ep, text="Clase de armadura:", font=("Garamond", 16), background='#F4F1DE')
        self.armor_class_label.grid(row=4, column=4, padx=(25, 5), pady=5, sticky=tk.NSEW)
        self.armor_class_info_label = ttk.Label(frame_ep, text="", font=("Garamond", 14), background='#F4F1DE')
        self.armor_class_info_label.grid(row=4, column=5, padx=(5, 20), pady=5, sticky=tk.NSEW)

        # Dado de daño
        self.hit_dice_label = ttk.Label(frame_ep, text="Dado de daño:", font=("Garamond", 16), background='#F4F1DE')
        self.hit_dice_label.grid(row=5, column=4, padx=(25, 5), pady=(5, 25), sticky=tk.NSEW)
        self.hit_dice_info_label = ttk.Label(frame_ep, text="", font=("Garamond", 14), background='#F4F1DE')
        self.hit_dice_info_label.grid(row=5, column=5, padx=(5, 20), pady=(5, 25), sticky=tk.NSEW)

        self.combobox_race.bind("<<ComboboxSelected>>", self.update_race_bonuses)

        #Idiomas
        languages_frame = ttk.Frame(frame_ep, style='Custom.TLabelframe')
        languages_frame.grid(row=1, rowspan=5, column=9, columnspan=3, padx=(80, 5), pady=15, sticky="nsew")

        self.languages_label = create_taped_label(languages_frame, "Idiomas")
        self.languages_label.grid(columnspan=2, padx=(30, 30), pady=5, sticky=tk.NSEW)
        self.languages_info_label = ttk.Label(languages_frame, text="", font=("Garamond", 14), background='#F4F1DE', wraplength=150)
        self.languages_info_label.grid(row=1, rowspan=3, column=0, padx=(30, 30), pady=5, sticky=tk.NSEW)

        # Atributos
        attributes = ttk.Frame(central_frame, style='Custom.TFrame')
        attributes.grid(row=6, column=0, columnspan=1, padx=(25, 15), pady=(20, 0), sticky="nsew")

        # Fuerza
        strength = ttk.Frame(attributes, style='Custom.TFrame')
        strength.grid(row=0, column=0, padx=5, pady=(0, 5), sticky=tk.NSEW)

        self.strength_label = create_taped_label(strength, "Fuerza")
        self.strength_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.strength_entry = ttk.Entry(strength, font=("Garamond", 18), width=5)
        self.strength_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.strength_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.strength_info = ttk.Label(strength, text="", font=("Garamond", 10), background='#F4F1DE')
        self.strength_info.grid(row=1, column=1, padx=(5,0), pady=5, sticky=tk.NSEW)
        self.strength_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Destreza
        dexterity = ttk.Frame(attributes, style='Custom.TFrame')
        dexterity.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.dexterity_label = create_taped_label(dexterity, "Destreza")
        self.dexterity_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.dexterity_entry = ttk.Entry(dexterity, font=("Garamond", 18), width=5)
        self.dexterity_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.dexterity_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.dexterity_info = ttk.Label(dexterity, text="", font=("Garamond", 10), background='#F4F1DE')
        self.dexterity_info.grid(row=1, column=1, padx=(5,0), pady=5, sticky=tk.NSEW)
        self.dexterity_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Constitución
        constitution = ttk.Frame(attributes, style='Custom.TFrame')
        constitution.grid(row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.constitution_label = create_taped_label(constitution,"Constitución")
        self.constitution_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.constitution_entry = ttk.Entry(constitution, font=("Garamond", 18), width=5)
        self.constitution_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.constitution_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.constitution_info = ttk.Label(constitution, text="", font=("Garamond", 10), background='#F4F1DE')
        self.constitution_info.grid(row=1, column=1, padx=(5,0), pady=5, sticky=tk.NSEW)
        self.constitution_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Inteligencia
        intelligence = ttk.Frame(attributes, style='Custom.TFrame')
        intelligence.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.intelligence_label = create_taped_label(intelligence, "Inteligencia")
        self.intelligence_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.intelligence_entry = ttk.Entry(intelligence, font=("Garamond", 18), width=5)
        self.intelligence_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.intelligence_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.intelligence_info = ttk.Label(intelligence, text="", font=("Garamond", 10), background='#F4F1DE')
        self.intelligence_info.grid(row=1, column=1, padx=(5,0), pady=5, sticky=tk.NSEW)
        self.intelligence_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Sabiduría
        wisdom = ttk.Frame(attributes, style='Custom.TFrame')
        wisdom.grid(row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.wisdom_label = create_taped_label(wisdom, "Sabiduría")
        self.wisdom_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.wisdom_entry = ttk.Entry(wisdom, font=("Garamond", 18), width=5)
        self.wisdom_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.wisdom_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.wisdom_info = ttk.Label(wisdom, text="", font=("Garamond", 10), background='#F4F1DE')
        self.wisdom_info.grid(row=1, column=1, padx=(5, 0), pady=5, sticky=tk.NSEW)
        self.wisdom_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Carisma
        charisma = ttk.Frame(attributes, style='Custom.TFrame')
        charisma.grid(row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.charisma_label = create_taped_label(charisma, "Carisma")
        self.charisma_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.charisma_entry = ttk.Entry(charisma, font=("Garamond", 18), width=5)
        self.charisma_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.charisma_entry.bind("<KeyRelease>", lambda event: self.update_skill_modifiers())

        self.charisma_info = ttk.Label(charisma, text="", font=("Garamond", 10), background='#F4F1DE')
        self.charisma_info.grid(row=1, column=1, padx=(5, 0), pady=5, sticky=tk.NSEW)
        self.charisma_entry.bind("<KeyRelease>", self.update_saving_throws)

        # Crear el frame para las habilidades con Checkbuttons
        skills_frame = ttk.Frame(central_frame, style='Custom.TFrame')
        skills_frame.grid(row=6, column=1, rowspan=6, columnspan=2, padx=5, pady=(15, 0), sticky="nsew")

        # Llama a populate_skills después de crear el frame

        self.skills_label = create_taped_label(skills_frame, "Habilidades:")
        self.skills_label.grid(row=0, column=0, padx=(0, 15), pady=5, sticky=tk.NSEW)

        self.skill_vars = {}
        self.populate_skills(skills_frame)

        # Segundo Frame
        second_frame = ttk.Frame(central_frame, style='Custom.TFrame')
        second_frame.grid(row=6, column=3, rowspan=2, columnspan=5, padx=(15,5), pady=(5, 0), sticky="nsew")

        # Trasfondo
        self.background = get_backgrounds()
        self.label_background = create_taped_label(second_frame, "Trasfondo")
        self.label_background.grid(row=0, column=0, padx=(25, 30), pady=5, sticky=tk.NSEW)
        self.combobox_background = ttk.Combobox(second_frame, values=list(self.background.keys()), font=('Garamond', 15),
                                                state='readonly')
        self.combobox_background.grid(row=1, column=0, padx=(25, 30), pady=(5, 90), sticky=tk.NSEW)

        self.combobox_background.bind("<<ComboboxSelected>>", self.background_features)

        self.equipment_label = create_taped_label(second_frame, "Armadura")
        self.equipment_label.grid(row=0, column=1, columnspan=2, padx=(25, 30), pady=5, sticky=tk.NSEW)
        self.combobox_equipment = ttk.Combobox(second_frame, font=("Garamond", 14), state='readonly')
        self.combobox_equipment.grid(row=1, column=1, columnspan=2, padx=(25, 30), pady=(5, 90), sticky=tk.NSEW)

        self.combobox_equipment.bind("<<ComboboxSelected>>", self.update_armor_class)

        # Definir el inventario
        inventory_frame = ttk.Frame(second_frame, style='Custom.TLabelframe')
        inventory_frame.grid(row=3, column=2, rowspan=5, padx=(25, 30), pady=5, sticky="nsew")

        self.inventory_label = create_taped_label(inventory_frame, "Inventario")
        self.inventory_label.grid(row=0, column=0, columnspan=2, padx=(25, 30), pady=5, sticky=tk.NSEW)
        self.inventory_info_label = ttk.Label(inventory_frame, text="", font=("Garamond", 12), background='#F4F1DE',
                                              wraplength=200)
        self.inventory_info_label.grid(row=2, column=0, columnspan=2, padx=(25, 30), pady=5, sticky=tk.NSEW)

        # Crear el filtro de categoría de ítems en el inventario
        self.categories = ["Todos"] + get_categories()  # "Todos" es la primera opción
        self.combobox_category = ttk.Combobox(inventory_frame, values=self.categories, font=("Garamond", 14),
                                              state='readonly')
        self.combobox_category.grid(row=1, column=0, columnspan=2, padx=(25, 30), pady=(5, 5), sticky=tk.NSEW)
        self.combobox_category.bind("<<ComboboxSelected>>", self.update_inventory)

        # Crear el frame para las tiradas de salvación
        saving_throws_frame = ttk.Frame(second_frame, style='Custom.TLabelframe')
        saving_throws_frame.grid(row=3, column=0, padx=(25, 30), pady=5, sticky="nsew")

        # Crear el label y el contenido dentro del nuevo frame
        self.saving_throws = create_taped_label(saving_throws_frame, "Tiradas de salvación")
        self.saving_throws.grid(row=0, column=0, padx=(25, 30), pady=5, sticky='w')

        self.saving_throws_info_label = ttk.Label(saving_throws_frame, text="", font=("Garamond", 12),
                                                  background='#F4F1DE',
                                                  wraplength=200)
        # Aumenta el padding vertical para más espacio entre los atributos
        self.saving_throws_info_label.grid(row=1, column=0, padx=(25, 30), pady=10, sticky="nsew")

        self.update_saving_throws()

        #Características del trasfondo
        background_features = ttk.Frame(central_frame, style='Custom.TLabelframe')
        background_features.grid(row=6, column=8, rowspan=12, columnspan=2, padx=(15,5), pady=(5, 0), sticky="nsew" )

        self.ideal_label = create_taped_label(background_features, "Ideal")
        self.ideal_label.grid(row=0, column=0, padx=30, pady=(30, 5), sticky=tk.NSEW)
        self.ideal_info_label = ttk.Label(background_features, text="", font=("Garamond", 12), background='#F4F1DE', wraplength=150)
        self.ideal_info_label.grid(row=1, rowspan=5, column=0, padx=30, pady=5, sticky=tk.NSEW)

        self.flaw_label = create_taped_label(background_features, "Defecto")
        self.flaw_label.grid(row=6, column=0, padx=30, pady=5, sticky=tk.NSEW)
        self.flaw_info_label = ttk.Label(background_features, text="", font=("Garamond", 12), background='#F4F1DE', wraplength=150)
        self.flaw_info_label.grid(row=7, rowspan=3, column=0, padx=30, pady=5, sticky=tk.NSEW)

        self.traits_label = create_taped_label(background_features, "Rasgos de Personalidad")
        self.traits_label.grid(row=10, column=0, padx=30, pady=5, sticky=tk.NSEW)
        self.traits_info_label = ttk.Label(background_features, text="", font=("Garamond", 12), background='#F4F1DE', wraplength=150)
        self.traits_info_label.grid(row=11, rowspan=3, column=0, padx=30, pady=5, sticky=tk.NSEW)

        self.bond_label = create_taped_label(background_features, "Vínculo")
        self.bond_label.grid(row=14, column=0, padx=30, pady=5, sticky=tk.NSEW)
        self.bond_info_label = ttk.Label(background_features, text="", font=("Garamond", 12), background='#F4F1DE', wraplength=150)
        self.bond_info_label.grid(row=15, rowspan=3, column=0, padx=30, pady=(5, 30), sticky=tk.NSEW)

    def select_image(self):
        # Abrir cuadro de diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        if file_path:
            # Cargar imagen usando PIL
            image = Image.open(file_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Guardar la ruta de la imagen seleccionada
            self.selected_image_path = file_path

            # Reemplazar el botón con el widget de imagen
            self.add_image_button.place_forget()
            self.img_label = tk.Label(self.image_frame, image=photo)
            self.img_label.image = photo  # Mantener una referencia a la imagen para evitar que se elimine
            self.img_label.place(relx=0.5, rely=0.5, anchor="center")

    def db_query(self, consulta, parametros=()):
        with sqlite3.connect(self.db_characters) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def validate_attributes(self):
        try:
            attributes = [
                int(self.strength_entry.get()),
                int(self.dexterity_entry.get()),
                int(self.constitution_entry.get()),
                int(self.intelligence_entry.get()),
                int(self.wisdom_entry.get()),
                int(self.charisma_entry.get())
            ]
        except ValueError:
            messagebox.showerror("Error de validación", "Todos los atributos deben ser números enteros.")
            return False

        total_sum = sum(attributes)

        if any(attr < 8 or attr > 15 for attr in attributes):
            messagebox.showerror("Error de validación", "Cada atributo debe estar entre 8 y 15.")
            return False

        if total_sum != 75:
            messagebox.showerror("Error de validación",
                                 f'La suma de todos los atributos debe ser exactamente 75. Actualmente sumas {total_sum} puntos.')
            return False

        return True

    def update_race_bonuses(self, event=None):
        selected_race = self.combobox_race.get()
        bonuses = self.race_bonuses.get(selected_race, {})

        self.strength_info.config(text=f"+{bonuses.get('Fuerza', 0)}")
        self.dexterity_info.config(text=f"+{bonuses.get('Destreza', 0)}")
        self.constitution_info.config(text=f"+{bonuses.get('Constitución', 0)}")
        self.intelligence_info.config(text=f"+{bonuses.get('Inteligencia', 0)}")
        self.wisdom_info.config(text=f"+{bonuses.get('Sabiduría', 0)}")
        self.charisma_info.config(text=f"+{bonuses.get('Carisma', 0)}")
        self.speed_info_label.config(text=f"{bonuses.get('Velocidad', 0)}")

        self.update_languages()

    def highlight_class_skills(self, event=None):
        selected_class = self.combobox_c_class.get()

        # Limpiar todas las selecciones de habilidades y resetear a estado normal
        for skill_name, skill_data in self.skill_vars.items():
            skill_data['var'].set(False)  # Desmarcar los checkboxes
            skill_data['label'].config(font=("Garamond", 11, "normal"))  # Resetear la fuente a normal
            skill_data['cb'].config(state=tk.NORMAL)  # Habilitar todos los checkboxes

        # Obtener y resaltar las habilidades de la clase seleccionada
        class_skills = get_class_skills(selected_class)
        for skill_name, skill_data in self.skill_vars.items():
            if skill_name in class_skills:
                skill_data['label'].config(font=("Garamond", 11, "bold"))
                skill_data['cb'].config(state=tk.NORMAL)  # Habilitar los checkboxes de las habilidades disponibles
            else:
                skill_data['label'].config(font=("Garamond", 11, "normal"))
                skill_data['cb'].config(
                    state=tk.DISABLED)  # Desactivar los checkboxes de las habilidades no disponibles

        # Mostrar un pop-up con el número de habilidades que pueden seleccionarse
        max_skills = get_class_max_skills(selected_class)
        messagebox.showinfo("Habilidades", f"Puedes seleccionar {max_skills} habilidades de entre las que están en negrita.")
        self.on_skill_toggle()

        # Ahora, actualizar el combobox de armaduras
        armor_names = get_class_armors(selected_class)
        self.combobox_equipment['values'] = armor_names
        if armor_names:
            self.combobox_equipment.current(0)
            self.update_armor_class()
        else:
            self.combobox_equipment.set("Sin armadura")

        # Hit dice:
        hit_dice = get_classes()[
            selected_class]  # Aquí obtenemos el golpe de daño (hit dice) de la clase seleccionada
        self.hit_dice_info_label.config(text=f"{hit_dice['Hit dice']}")  # Asegúrate de usar la clave correcta

        self.update_inventory()

    def update_languages(self, event=None):
        selected_background = self.combobox_background.get()
        background_languages = get_background_languages(selected_background)

        selected_race = self.combobox_race.get()
        race_languages = get_race_languages(selected_race)

        # Combinar los idiomas del trasfondo y la clase en un solo conjunto
        all_languages = set(background_languages + race_languages)

        # Mostrar los idiomas en la etiqueta correspondiente
        self.languages_info_label.config(text='\n'.join(all_languages) if all_languages else "Sin idiomas")
        self.languages_info_label.grid(row=1, column=0, padx=(25, 30), pady=10, sticky=tk.NSEW)  # Cambia el valor de pady

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

    def update_inventory(self, event=None):
        selected_class = self.combobox_c_class.get()
        class_items = get_class_items(selected_class)

        selected_background = self.combobox_background.get()
        background_items = get_background_items(selected_background)

        # Obtener la categoría seleccionada
        selected_category = self.combobox_category.get()

        # Filtrar los items de la clase y el trasfondo según la categoría seleccionada
        if selected_category and selected_category != "Todos":
            all_items = [item for item in class_items + background_items if
                         self.get_item_category(item) == selected_category]
        else:
            all_items = class_items + background_items

        # Actualizar la etiqueta del inventario
        self.inventory_info_label.config(text="")  # Borra el texto primero
        self.inventory_info_label.config(text='\n'.join(all_items) if all_items else "Sin objetos")

    def get_item_category(self, item_name):
        db_path = self.db_characters

        query = '''
            SELECT c.name 
            FROM categories c 
            JOIN items i ON c.id = i.category_id 
            WHERE i.name = ?
        '''

        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            cursor.execute(query, (item_name,))
            result = cursor.fetchone()

            if result:
                print(f"Categoría del ítem '{item_name}': {result[0]}")  # Agrega esta línea para depuración
                return result[0]  # Retorna el nombre de la categoría
            else:
                print(f"No se encontró la categoría para el ítem '{item_name}'")  # Depuración
                return None

    def update_armor_class(self, event=None):
        selected_armor = self.combobox_equipment.get()
        armor_class = get_armor_class(selected_armor)

        if armor_class is not None:
            self.armor_class_info_label.config(text=str(armor_class))
        else:
            self.armor_class_info_label.config(text="Sin armadura")

    def populate_skills(self, parent_frame):
        skills = get_skills()  # Obtén la lista de habilidades desde la base de datos

        # Itera sobre las habilidades y crea un Checkbutton para cada una
        row = 1  # Asegúrate de comenzar en la primera fila
        for skill, attribute in skills.items():
            skill_var = tk.BooleanVar()  # Crea una variable para el estado del checkbutton

            # Vincular la función on_skill_toggle al evento de cambio de estado
            skill_var.trace_add('write', self.on_skill_toggle)

            # Crear un sub-frame para cada par de Checkbutton y etiqueta
            skill_frame = tk.Frame(parent_frame, bg='#F4F1DE')  # Fondo igual que el del parent_frame
            skill_frame.grid(row=row, column=0, pady=2, sticky=tk.NSEW)

            # Crea un Checkbutton y lo añade al sub-frame
            cb = tk.Checkbutton(skill_frame, variable=skill_var, onvalue=True, offvalue=False, bg='#F4F1DE')
            cb.pack(side="left")  # Usar pack para que se alinee junto con la etiqueta sin separación

            # Crea una etiqueta para el Checkbutton
            bonus = ()
            skill_label = tk.Label(skill_frame, text=f"{skill} ({attribute})", font=("Garamond", 12),
                                   background='#F4F1DE')
            skill_label.pack(side="left")  # Usar pack para alinearlo a la izquierda del Checkbutton

            self.skill_vars[skill] = {'var': skill_var, 'label': skill_label, 'cb': cb, 'attribute': attribute}

            row += 1  # Mover a la siguiente fila

    def on_skill_toggle(self, *args):
        # Obtener el máximo de habilidades permitidas para la clase seleccionada
        max_skills = get_class_max_skills(self.combobox_c_class.get())

        if max_skills is not None:
            # Contar cuántas habilidades están seleccionadas
            selected_count = sum(skill_data['var'].get() for skill_data in self.skill_vars.values())
            # Si se ha alcanzado el máximo, deshabilitar las habilidades no seleccionadas
            if selected_count >= max_skills:
                for skill_name, skill_data in self.skill_vars.items():
                    if not skill_data['var'].get():  # Deshabilitar solo las no seleccionadas
                        skill_data['cb'].config(state=tk.DISABLED)
                self.update_skill_modifiers()
            else:
                # Si no se ha alcanzado el máximo, habilitar todas las habilidades permitidas
                for skill_name, skill_data in self.skill_vars.items():
                    # Obtener la fuente actual y verificar que contiene 'bold'
                    current_font = skill_data['label'].cget('font')
                    if 'bold' in current_font:  # Verificar que la fuente contiene 'bold'
                        skill_data['cb'].config(state=tk.NORMAL)
                self.update_skill_modifiers()

    def update_skill_modifiers(self):
        # Bonificador de competencia fijo para personajes de nivel 1
        proficiency_bonus = 2

        # Obtener los atributos
        strength = calculate_modifier(int(self.strength_entry.get() or 0))
        dexterity = calculate_modifier(int(self.dexterity_entry.get() or 0))
        constitution = calculate_modifier(int(self.constitution_entry.get() or 0))
        intelligence = calculate_modifier(int(self.intelligence_entry.get() or 0))
        wisdom = calculate_modifier(int(self.wisdom_entry.get() or 0))
        charisma = calculate_modifier(int(self.charisma_entry.get() or 0))

        # Diccionario para asignar los modificadores según la habilidad
        attribute_modifiers = {
            "Fuerza": strength,
            "Destreza": dexterity,
            "Constitución": constitution,
            "Inteligencia": intelligence,
            "Sabiduría": wisdom,
            "Carisma": charisma
        }

        # Iterar sobre las habilidades y actualizar las etiquetas
        for skill, data in self.skill_vars.items():
            # Obtener el atributo asociado a la habilidad
            skill_attribute = data['attribute']  # Usamos el atributo almacenado en populate_skills()

            # Obtener el modificador del atributo correspondiente
            base_modifier = attribute_modifiers.get(skill_attribute, 0)

            # Si la habilidad está seleccionada, se le añade el bonificador de competencia
            if data['var'].get():
                total_modifier = base_modifier + proficiency_bonus
            else:
                total_modifier = 0

            if total_modifier != 0:
                data['label'].config(text=f"{skill} ({skill_attribute}) +{total_modifier}")
            else:
                data['label'].config(text=f"{skill} ({skill_attribute})")

    def background_features(self, event=None):
        selected_background = self.combobox_background.get()
        features = self.background.get(selected_background, {})

        # Asignar los valores de los ideales, defectos, etc.
        self.ideal_info_label.config(text=features.get('Ideal', ''))
        self.flaw_info_label.config(text=features.get('Defecto', ''))
        self.traits_info_label.config(text=features.get('Rasgos de personalidad', ''))
        self.bond_info_label.config(text=features.get('Vínculo', ''))

        self.update_languages()
        self.update_inventory()

    def save_character(self):
        if not self.validate_attributes():
            return

        # Obtener el nombre del personaje
        character_name = self.entry_name.get()

        # Comprobar si se ha generado una imagen con la IA
        if hasattr(self, 'generated_image'):
            # Definir la ruta donde se guardará la imagen
            image_path = os.path.join('images', f"{character_name}.jpg")
            # Crear el directorio 'images' si no existe
            os.makedirs('images', exist_ok=True)
            # Guardar la imagen en el directorio especificado
            self.generated_image.save(image_path, format='JPEG')
            self.selected_image_path = image_path  # Guardar la ruta para su uso posterior

        # Insertar nuevo personaje en la tabla characters
        query = 'INSERT INTO characters (name, race_id, class_id, level, background_id, image_path) VALUES (?, ?, ?, ?, ?, ?)'
        parametros = (
            self.entry_name.get(),
            self.combobox_race.get(),
            self.combobox_c_class.get(),
            self.combobox_background.get(),
            self.entry_level.cget("text"),
            getattr(self, 'selected_image_path', None)
        )

        with sqlite3.connect(self.db_characters) as con:
            cursor = con.cursor()
            cursor.execute(query, parametros)
            character_id = cursor.lastrowid
            con.commit()

        # Guardar los atributos asociados
        self.save_attributes(character_id)

        # Guardar las habilidades seleccionadas
        self.save_skills(character_id)

        # Mensaje de confirmación y limpieza del formulario
        messagebox.showinfo("Éxito", f'Personaje {self.entry_name.get()} añadido con éxito')
        self.clear_form()

    def save_attributes(self, character_id):
        attributes = [
            ('Fuerza', self.strength_entry.get()),
            ('Destreza', self.dexterity_entry.get()),
            ('Constitución', self.constitution_entry.get()),
            ('Inteligencia', self.intelligence_entry.get()),
            ('Sabiduría', self.wisdom_entry.get()),
            ('Carisma', self.charisma_entry.get())
        ]

        for attr_name, attr_value in attributes:
            attr_id = self.db_query('SELECT id FROM attributes WHERE name = ?', (attr_name,)).fetchone()
            if attr_id:  # Verifica si se recuperó un ID válido
                attr_id = attr_id[0]  # Extrae el ID de la tupla
                self.db_query(
                    'INSERT INTO attribute_character_association (attribute_id, character_id, value) VALUES (?, ?, ?)',
                    (attr_id, character_id, attr_value)
                )

    def save_skills(self, character_id):
        for skill_name, skill_var in self.skill_vars.items():
            if isinstance(skill_var, tk.BooleanVar) and skill_var.get() == 1:  # Asegurarse de que el valor sea correcto
                skill_id = self.db_query('SELECT id FROM skills WHERE name = ?', (skill_name,)).fetchone()
                if skill_id:
                    skill_id = skill_id[0]
                    self.db_query(
                        'INSERT INTO skill_character_association (skill_id, character_id, value) VALUES (?, ?, ?)',
                        (skill_id, character_id, 1)
                    )

    def save_inventory(self, character_id):
        items_text  = self.inventory_info_label.cget("text")
        items = items_text.split('\n')
        items = [item.strip() for item in items if item.strip()]

        if items:
            for item in items:
                item_id = self.db_query('SELECT id FROM inventories WHERE name = ?', (item,)).fetchone()
                if item_id:
                    item_id = item_id[0]
                    # Insertar la asociación en la tabla character_inventory_association
                    self.db_query(
                        'INSERT INTO character_inventory_association (character_id, inventory_id) VALUES (?, ?)',
                        (character_id, item_id))

    def clear_form(self):
        # Limpiar el campo de nombre
        self.entry_name.delete(0, tk.END)

        # Restablecer los comboboxes de raza, clase y trasfondo
        self.combobox_race.set('')
        self.combobox_c_class.set('')
        self.combobox_background.set('')
        self.combobox_equipment.set('')
        self.combobox_category.set('Todos')  # Restablecer el filtro a "Todos"

        # Restablecer el nivel al valor inicial
        self.entry_level.config(text="1")

        # Limpiar los campos de atributos
        self.strength_entry.delete(0, tk.END)
        self.dexterity_entry.delete(0, tk.END)
        self.constitution_entry.delete(0, tk.END)
        self.intelligence_entry.delete(0, tk.END)
        self.wisdom_entry.delete(0, tk.END)
        self.charisma_entry.delete(0, tk.END)

        # Limpiar las bonificaciones raciales mostradas
        self.strength_info.config(text="")
        self.dexterity_info.config(text="")
        self.constitution_info.config(text="")
        self.intelligence_info.config(text="")
        self.wisdom_info.config(text="")
        self.charisma_info.config(text="")
        self.speed_info_label.config(text="")

        # Limpiar la imagen seleccionada
        if hasattr(self, 'img_label'):
            self.img_label.destroy()
        self.selected_image_path = None
        self.add_image_button.place(relx=0.5, rely=0.5,
                                    anchor="center")  # Mostrar el botón de agregar imagen nuevamente

        # Limpiar las habilidades seleccionadas y restablecer los textos y el estado de los Checkbuttons
        for skill_name, skill_data in self.skill_vars.items():
            skill_data['var'].set(False)
            skill_data['label'].config(text=f"{skill_name} ({skill_data['attribute']})",
                                       font=("Garamond", 12, "normal"))
            skill_data['cb'].config(state=tk.NORMAL)  # Habilitar todos los checkboxes de habilidades

        # Limpiar el inventario
        self.inventory_info_label.config(text="")

        # Limpiar la clase de armadura
        self.armor_class_info_label.config(text="")

        # Limpiar tiradas de salvación
        self.saving_throws_info_label.config(text="")

        # Limpiar los idiomas mostrados
        self.languages_info_label.config(text="")

        #Limpiar el dado de daño:
        self.hit_dice_info_label.config(text="")

        # Limpiar los campos de características del trasfondo
        self.ideal_info_label.config(text="")
        self.flaw_info_label.config(text="")
        self.traits_info_label.config(text="")
        self.bond_info_label.config(text="")