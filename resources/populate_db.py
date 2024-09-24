from db import session
from models import *


# Datos para poblar las tablas
attributes = [
    {"name": "Fuerza"},
    {"name": "Destreza"},
    {"name": "Constitución"},
    {"name": "Inteligencia"},
    {"name": "Sabiduría"},
    {"name": "Carisma"}
]

skills = [
    {"name": "Acrobacias", "attribute": "Destreza"},
    {"name": "Manejo de Animales", "attribute": "Sabiduría"},
    {"name": "Arcano", "attribute": "Inteligencia"},
    {"name": "Atletismo", "attribute": "Fuerza"},
    {"name": "Engaño", "attribute": "Carisma"},
    {"name": "Historia", "attribute": "Inteligencia"},
    {"name": "Perspicacia", "attribute": "Sabiduría"},
    {"name": "Intimidación", "attribute": "Carisma"},
    {"name": "Investigación", "attribute": "Inteligencia"},
    {"name": "Medicina", "attribute": "Sabiduría"},
    {"name": "Naturaleza", "attribute": "Inteligencia"},
    {"name": "Percepción", "attribute": "Sabiduría"},
    {"name": "Interpretación", "attribute": "Carisma"},
    {"name": "Persuasión", "attribute": "Carisma"},
    {"name": "Religión", "attribute": "Inteligencia"},
    {"name": "Juego de Manos", "attribute": "Destreza"},
    {"name": "Sigilo", "attribute": "Destreza"},
    {"name": "Supervivencia", "attribute": "Sabiduría"}
]

races = [
    {"name": "Humano", "speed": 30, "extra_strength": 1, "extra_dexterity": 1, "extra_constitution": 1,
     "extra_intelligence": 1, "extra_wisdom": 1, "extra_charisma": 1, "languages": ["Común", "Otro idioma a elección"],
     "subraces": [], "skills": []},

    {"name": "Elfo", "speed": 30, "extra_dexterity": 2, "extra_strength": 0, "extra_constitution": 0,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Élfico"],
     "skills": ["Percepción"]},

    {"name": "Enano", "speed": 25, "extra_strength": 0, "extra_dexterity": 0, "extra_constitution": 2,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Enano"],
     "skills": ["Historia"]},

    {"name": "Mediano", "speed": 25, "extra_strength": 0, "extra_dexterity": 2, "extra_constitution": 0,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Mediano"],
     "skills": ["Sigilo"]},

    {"name": "Gnomo", "speed": 25, "extra_strength": 0, "extra_dexterity": 0, "extra_constitution": 0,
     "extra_intelligence": 2, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Gnomo"],
     "skills": ["Investigación"]},

    {"name": "Semielfo", "speed": 30, "extra_strength": 0, "extra_dexterity": 0, "extra_constitution": 0,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 2,
     "languages": ["Común", "Élfico", "Un idioma extra a elección"],
     "subraces": [], "skills": ["Persuasión", "Engaño"]},

    {"name": "Semiorco", "speed": 30, "extra_strength": 2, "extra_dexterity": 0, "extra_constitution": 1,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Orco"],
     "subraces": [], "skills": ["Intimidación"]},

    {"name": "Tiefling", "speed": 30, "extra_strength": 0, "extra_dexterity": 0, "extra_constitution": 0,
     "extra_intelligence": 1, "extra_wisdom": 0, "extra_charisma": 2, "languages": ["Común", "Infernal"],
     "subraces": [], "skills": ["Engaño"]},

    {"name": "Dracónido", "speed": 30, "extra_strength": 2, "extra_dexterity": 0, "extra_constitution": 0,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 1, "languages": ["Común", "Dracónico"],
     "subraces": [], "skills": []},

    {"name": "Medioorco", "speed": 30, "extra_strength": 2, "extra_dexterity": 0, "extra_constitution": 1,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 0, "languages": ["Común", "Orco"],
     "subraces": [], "skills": ["Intimidación"]},

    {"name": "Medioelfo", "speed": 30, "extra_strength": 0, "extra_dexterity": 0, "extra_constitution": 0,
     "extra_intelligence": 0, "extra_wisdom": 0, "extra_charisma": 2,
     "languages": ["Común", "Élfico", "Un idioma extra a elección"],
     "subraces": [], "skills": ["Persuasión", "Engaño"]},
]

languages = [
    {"name": "Común"},
    {"name": "Élfico"},
    {"name": "Enano"},
    {"name": "Mediano"},
    {"name": "Gnomo"},
    {"name": "Orco"},
    {"name": "Infernal"},
    {"name": "Celestial"},
    {"name": "Primordial"},
    {"name": "Gigante"},
    {"name": "Dracónico"},
    {"name": "Aquan"},
    {"name": "Auran"},
    {"name": "Un idioma extra a elección"}
]

classes = [
    {"name": "Bárbaro", "hit_dice": "d12", "armor": ["Ligera", "Mediana", "Escudo"],
     "weapons": "Armas simples, armas marciales",
     "skills": ["Atletismo", "Intimidación", "Supervivencia", "Percepción"],
     "items": ["Hacha de mano", "Gran hacha", "Paquete de aventurero"],
     "max_skills": 2,
     "saving_throws": ["Fuerza", "Constitución"]},

    {"name": "Bardo", "hit_dice": "d8", "armor": ["Ligera"],
     "weapons": "Armas simples, ballestas de mano, espadas largas, estoques, espadas cortas",
     "skills": ["Acrobacias", "Atletismo", "Engaño", "Interpretación", "Intimidación", "Juego de Manos",
                "Perspicacia", "Persuasión", "Religión", "Sigilo"],
     "items": ["Daga", "Ballesta de mano", "Paquete de músico", "Tres instrumentos musicales a tu elección"],
     "max_skills": 3,
     "saving_throws": ["Destreza", "Carisma"]},

    {"name": "Clérigo", "hit_dice": "d8", "armor": ["Ligera", "Mediana", "Escudo"],
     "weapons": "Armas simples",
     "skills": ["Historia", "Perspicacia", "Medicina", "Persuasión", "Religión"],
     "items": ["Maza", "Escudo", "Paquete de sacerdote"],
     "max_skills": 2,
     "saving_throws": ["Sabiduría", "Carisma"]},

    {"name": "Druida", "hit_dice": "d8", "armor": ["Ligera", "Mediana", "Escudo"],
     "weapons": "Armas de palo, dardos, mazas, jabalinas, porras, hoces, hondas, lanzas",
     "skills": ["Arcano", "Perspicacia", "Medicina", "Religión", "Naturaleza", "Supervivencia"],
     "items": ["Sickle", "Paquete de explorador", "Herboristería"],
     "max_skills": 2,
     "saving_throws": ["Inteligencia", "Sabiduría"]},

    {"name": "Guerrero", "hit_dice": "d10", "armor": ["Ligera", "Mediana", "Pesada", "Escudo"],
     "weapons": "Armas simples, armas marciales",
     "skills": ["Acrobacias", "Atletismo", "Historia", "Intimidación", "Percepción", "Supervivencia"],
     "items": ["Espada larga", "Escudo", "Paquete de aventurero"],
     "max_skills": 2,
     "saving_throws": ["Fuerza", "Constitución"]},

    {"name": "Monje", "hit_dice": "d8", "armor": [], "weapons": "Armas simples, espadas cortas",
     "skills": ["Acrobacias", "Atletismo", "Historia", "Juego de Manos", "Religión", "Sigilo"],
     "items": ["Dardo", "Paquete de aventurero", "Un tipo de herramienta de artesano o Instrumentos Musicales"],
     "max_skills": 2,
     "saving_throws": ["Fuerza", "Destreza"]},

    {"name": "Paladín", "hit_dice": "d10", "armor": ["Ligera", "Mediana", "Pesada", "Escudo"],
     "weapons": "Armas simples, armas marciales",
     "skills": ["Atletismo", "Intimidación", "Medicina", "Perspicacia", "Religión"],
     "items": ["Espada larga", "Escudo", "Paquete de sacerdote"],
     "max_skills": 2,
     "saving_throws": ["Sabiduría", "Carisma"]},

    {"name": "Explorador", "hit_dice": "d10", "armor": ["Ligera", "Mediana", "Escudo"],
     "weapons": "Armas simples, armas marciales",
     "skills": ["Atletismo", "Investigación", "Naturaleza", "Percepción", "Sigilo", "Supervivencia"],
     "items": ["Arco largo", "Flechas", "Paquete de explorador"],
     "max_skills": 3,
     "saving_throws": ["Fuerza", "Destreza"]},

    {"name": "Pícaro", "hit_dice": "d8", "armor": ["Ligera"],
     "weapons": "Armas simples, ballestas de mano, espadas largas, estoques, espadas cortas",
     "skills": ["Acrobacias", "Atletismo", "Engaño", "Interpretación", "Intimidación",
                "Juego de Manos", "Percepción", "Sigilo"],
     "items": ["Daga", "Paquete de ladrón", "Herramientas de ladrón"],
     "max_skills": 4,
     "saving_throws": ["Destreza", "Inteligencia"]},

    {"name": "Hechicero", "hit_dice": "d6", "armor": [],
     "weapons": "Dagas, dardos, hondas, bastones, ballestas ligeras",
     "skills": ["Arcano", "Engaño", "Intimidación", "Persuasión", "Religión"],
     "items": ["Bastón", "Paquete de explorador"],
     "max_skills": 2,
     "saving_throws": ["Constitución", "Carisma"]},

    {"name": "Brujo", "hit_dice": "d8", "armor": ["Ligera"],
     "weapons": "Armas simples",
     "skills": ["Arcano", "Engaño", "Intimidación", "Perspicacia", "Religión"],
     "items": ["Daga", "Libro de hechizos", "Paquete de erudito"],
     "max_skills": 2,
     "saving_throws": ["Sabiduría", "Carisma"]},

    {"name": "Mago", "hit_dice": "d6", "armor": [],
     "weapons": "Dagas, dardos, hondas, bastones, ballestas ligeras",
     "skills": ["Arcano", "Historia", "Investigación", "Intimidación", "Religión"],
     "items": ["Bastón", "Libro de hechizos", "Paquete de erudito"],
     "max_skills": 2,
     "saving_throws": ["Inteligencia", "Sabiduría"]}
]

categories = [
    {"name": "Arma"},
    {"name": "Herramienta"},
    {"name": "Armas Marciales"},
    {"name": "Herramientas de Ladrón"},
    {"name": "Instrumentos Musicales"},
    {"name": "Paquete"},
    {"name": "Libros"},
    {"name": "Bastones"},
    {"name": "Paquete"},
    {"name": "Ropa"},
    {"name": "Vehículo de agua"},
    {"name": "Accesorio"},
    {"name": "Juego"},
    {"name": "Documento"},
    {"name": "Arma Simple"},
    {"name": "Documento"},
    {"name": "Vehículo"},
    {"name": "Escudo"}
    
]

items = [
    # Generales
    {"name": "Hacha de mano",
     "description": "Un hacha pequeña utilizada para combate cercano o trabajo.",
     "category": "Arma Simple"},
    {"name": "Gran hacha",
     "description": "Un hacha grande utilizada para infligir mayor daño en combate.",
     "category": "Armas Marciales"},
    {"name": "Paquete de aventurero",
     "description": "Un conjunto de herramientas y objetos utilizados por aventureros.",
     "category": "Paquete"},
    {"name": "Daga", "description": "Una pequeña arma usada para combate cercano.",
     "category": "Arma Simple"},
    {"name": "Ballesta de mano",
     "description": "Una ballesta compacta utilizada para disparar proyectiles.",
     "category": "Armas Marciales"},
    {"name": "Paquete de músico",
     "description": "Un conjunto de herramientas y objetos utilizados por músicos.",
     "category": "Paquete"},
    {"name": "Tres instrumentos musicales a tu elección",
     "description": "Tres instrumentos seleccionados por el usuario.",
     "category": "Instrumentos Musicales"},
    {"name": "Maza",
     "description": "Un arma contundente utilizada para el combate.",
     "category": "Arma Simple"},
    {"name": "Escudo",
     "description": "Un escudo utilizado para defensa en combate.",
     "category": "Escudo"},
    {"name": "Paquete de sacerdote",
     "description": "Un conjunto de herramientas y objetos utilizados por sacerdotes.",
     "category": "Paquete"},
    {"name": "Sickle", "description": "Una hoz pequeña utilizada como arma o herramienta.",
     "category": "Arma Simple"},
    {"name": "Herboristería", "description": "Herramientas utilizadas para preparar remedios herbales.",
     "category": "Herramienta"},
    {"name": "Espada larga", "description": "Una espada de tamaño mediano utilizada para combate.",
     "category": "Armas Marciales"},
    {"name": "Arco largo", "description": "Un arco utilizado para disparar flechas a larga distancia.",
     "category": "Armas Marciales"},
    {"name": "Flechas", "description": "Proyectiles utilizados para ser disparados con un arco.",
     "category": "Arma"},
    {"name": "Dardo", "description": "Un pequeño proyectil utilizado para ataques a distancia.",
     "category": "Arma Simple"},
    {"name": "Herramienta de artesano o Instrumentos Musicales", "description": "Una herramienta de trabajo artesanal o un Instrumentos Musicales.",
     "category": "Herramienta"},
    {"name": "Libro de hechizos", "description": "Un libro que contiene conjuros y hechizos.",
     "category": "Herramienta"},
    {"name": "Símbolo sagrado", "description": "Un símbolo sagrado utilizado para representar la devoción religiosa.",
     "category": "Herramienta"},
    {"name": "Libro de plegarias", "description": "Un libro con plegarias y escrituras religiosas.",
     "category": "Herramienta"},
    {"name": "5 inciensos", "description": "Cinco varitas de incienso usadas en rituales religiosos.",
     "category": "Herramienta"},
    {"name": "Ropajes", "description": "Ropas comunes que se utilizan para diferentes actividades cotidianas.",
     "category": "Ropa"},
    {"name": "Conjunto de disfraces", "description": "Una variedad de disfraces para cambiar de identidad.",
     "category": "Herramienta"},
    {"name": "Kit de disfraz", "description": "Un kit con elementos para crear disfraces.",
     "category": "Herramienta"},
    {"name": "Herramientas de falsificación", "description": "Herramientas utilizadas para crear documentos falsos.",
     "category": "Herramienta"},
    {"name": "Pata de cabra", "description": "Una herramienta metálica usada para hacer palanca.",
     "category": "Herramienta"},
    {"name": "Ropa de actuación", "description": "Ropa especial usada para actuaciones y espectáculos.",
     "category": "Ropa"},
    {"name": "Carta de presentación", "description": "Una carta que te presenta como un miembro respetable de la sociedad.",
     "category": "Documento"},
    {"name": "Capa", "description": "Una capa usada para protección o como prenda de vestir.",
     "category": "Ropa"},
    {"name": "Anillo de sello", "description": "Un anillo usado para sellar documentos importantes.",
     "category": "Accesorio"},
    {"name": "Un bastón", "description": "Un simple bastón de madera utilizado para caminar.",
     "category": "Arma Simple"},
    {"name": "Un trofeo", "description": "Un trofeo que simboliza una victoria o logro pasado.",
     "category": "Accesorio"},
    {"name": "Botella de tinta", "description": "Una pequeña botella de tinta para escribir.",
     "category": "Herramienta"},
    {"name": "Pluma", "description": "Una pluma utilizada para escribir con tinta.",
     "category": "Herramienta"},
    {"name": "Cuchillo pequeño", "description": "Un pequeño cuchillo utilizado para diversas tareas.",
     "category": "Arma Simple"},
    {"name": "Palo corto", "description": "Un bastón corto usado como arma o herramienta.",
     "category": "Arma Simple"},
    {"name": "50 pies de cuerda de cáñamo", "description": "Un largo trozo de cuerda resistente hecha de cáñamo.",
     "category": "Herramienta"},
    {"name": "Insignia de rango", "description": "Una insignia que indica el rango de un soldado.",
     "category": "Accesorio"},
    {"name": "Un dado", "description": "Un dado común utilizado en juegos de azar.",
     "category": "Juego"},
    {"name": "Mapa", "description": "Un mapa que muestra la geografía de una región.",
     "category": "Documento"},

    # Específicos de trasfondos
    {"name": "Paquete de sacerdote", "description": "Un conjunto de herramientas y objetos utilizados por sacerdotes.", "category": "Paquete"},
    {"name": "Paquete de embaucador", "description": "Herramientas y objetos utilizados para embaucar.", "category": "Paquete"},
    {"name": "Mochila", "description": "Una mochila utilizada para llevar objetos personales.", "category": "Accesorio"},
    {"name": "Tres instrumentos musicales", "description": "Tres instrumentos de elección utilizados por artistas.", "category": "Instrumentos Musicales"},
    {"name": "Carro", "description": "Un vehículo terrestre utilizado para transportar cargas.", "category": "Vehículo"},
    {"name": "Herramientas de artesano", "description": "Herramientas utilizadas por artesanos.", "category": "Herramienta"},
    {"name": "Paquete de gremio", "description": "Un conjunto de herramientas y objetos utilizados por miembros de un gremio.", "category": "Paquete"},
    {"name": "Kit de herbalismo", "description": "Un conjunto de herramientas utilizadas para la preparación de remedios herbales.", "category": "Herramienta"},
    {"name": "Ropa fina", "description": "Ropa de alta calidad, típicamente usada por nobles.", "category": "Ropa"},
    {"name": "Paquete de noble", "description": "Un conjunto de herramientas y objetos utilizados por nobles.", "category": "Paquete"},
    {"name": "Un Instrumentos Musicales", "description": "Un Instrumentos Musicales de elección.", "category": "Instrumentos Musicales"},
    {"name": "Paquete de explorador", "description": "Un conjunto de herramientas y objetos utilizados por exploradores.", "category": "Paquete"},
    {"name": "Paquete de erudito", "description": "Un conjunto de herramientas y objetos utilizados por eruditos.", "category": "Paquete"},
    {"name": "Paquete de marinero", "description": "Un conjunto de herramientas y objetos utilizados por marineros.", "category": "Paquete"},
    {"name": "Paquete de soldado", "description": "Un conjunto de herramientas y objetos utilizados por soldados.", "category": "Paquete"},
    {"name": "Paquete de huérfano", "description": "Un conjunto de herramientas y objetos utilizados por huérfanos.", "category": "Paquete"},
    {"name": "Vehículo de agua", "description": "Un vehículo utilizado para el transporte acuático.", "category": "Vehículo de agua"},
    {"name": "Herramientas de ladrón", "description": "Herramientas utilizadas por ladrones para diversas actividades delictivas.", "category": "Herramienta"},
    {"name": "Desactivación de trampas", "description": "Un conjunto de herramientas especializadas para desactivar trampas.", "category": "Herramienta"}
]

armors = [
    {"name": "Armadura de cuero", "armor_class": 11, "type": "Ligera", "strength": 0, "stealth": 0, "weight": 10.0},
    {"name": "Armadura acolchada", "armor_class": 11, "type": "Ligera", "strength": 0, "stealth": -1, "weight": 8.0},
    {"name": "Armadura de cuero tachonado", "armor_class": 12, "type": "Ligera", "strength": 0, "stealth": -1, "weight": 13.0},
    {"name": "Armadura de malla", "armor_class": 14, "type": "Media", "strength": 0, "stealth": -1, "weight": 40.0},
    {"name": "Armadura de escamas", "armor_class": 14, "type": "Media", "strength": 0, "stealth": -1, "weight": 45.0},
    {"name": "Armadura de media placa", "armor_class": 15, "type": "Media", "strength": 0, "stealth": -1, "weight": 50.0},
    {"name": "Armadura de piel", "armor_class": 11, "type": "Ligera", "strength": 0, "stealth": 1, "weight": 12.0},
    {"name": "Armadura de placas", "armor_class": 18, "type": "Pesada", "strength": 15, "stealth": -1, "weight": 65.0},
    {"name": "Armadura de anillas", "armor_class": 14, "type": "Media", "strength": 0, "stealth": -1, "weight": 55.0},
    {"name": "Cota de mallas", "armor_class": 16, "type": "Media", "strength": 13, "stealth": -1, "weight": 40.0},
    {"name": "Cota de escamas", "armor_class": 14, "type": "Media", "strength": 0, "stealth": -1, "weight": 45.0},
    {"name": "Armadura de cuero endurecido", "armor_class": 12, "type": "Ligera", "strength": 0, "stealth": 1, "weight": 14.0},
    {"name": "Armadura de anillas", "armor_class": 15, "type": "Media", "strength": 13, "stealth": -1, "weight": 60.0},
    {"name": "Armadura de peto", "armor_class": 14, "type": "Media", "strength": 0, "stealth": 1, "weight": 20.0},
    {"name": "Armadura de campo", "armor_class": 16, "type": "Pesada", "strength": 15, "stealth": -1, "weight": 70.0},
    {"name": "Armadura de cuero reforzado", "armor_class": 13, "type": "Ligera", "strength": 0, "stealth": 1, "weight": 15.0}
]

backgrounds = [
    {
        "name": "Acólito",
        "skills": ["Religión", "Perspicacia"],
        "languages": ["Común", "Celestial"],
        "items": ["Símbolo sagrado", "Libro de plegarias", "5 inciensos", "Ropajes", "Paquete de sacerdote"],
        "tool_proficiencies": "",
        "ideals": ["La tradición, las leyes y los rituales son fundamentales (Legal)", "La compasión es la mayor virtud (Bueno)"],
        "flaws": ["Yo tiendo a juzgar a los demás muy rápido"],
        "personality_traits": ["Soy amable y respetuoso", "Siempre estoy dispuesto a ayudar a los demás"],
        "bonds": ["Dedico mi vida a la iglesia y su comunidad"]
    },
    {
        "name": "Charlatán",
        "skills": ["Engaño", "Juego de Manos"],
        "languages": [],
        "items": ["Kit de disfraz", "Herramientas de falsificación", "Conjunto de disfraces", "Herramientas de falsificación", "Paquete de embaucador"],
        "tool_proficiencies": "Kit de disfraz, Herramientas de falsificación",
        "ideals": ["La independencia es la clave para el éxito (Caótico)", "Todo tiene un precio, y yo lo pongo (Neutral)"],
        "flaws": ["No puedo resistir el desafío de una apuesta"],
        "personality_traits": ["Me encanta la atención y soy un gran narrador", "Cambio de identidad como cambio de ropa"],
        "bonds": ["Tengo un gran secreto que no puedo revelar"]
    },
    {
        "name": "Criminal",
        "skills": ["Engaño", "Sigilo"],
        "languages": [],
        "items": ["Herramientas de ladrón", "Un tipo de juego", "Pata de cabra", "Mochila", "Paquete de ladrón"],
        "tool_proficiencies": "Herramientas de ladrón, Un tipo de juego",
        "ideals": ["La libertad es lo único que realmente importa (Caótico)", "Me importa más mi grupo que cualquier otra cosa (Neutral)"],
        "flaws": ["Haré cualquier cosa para escapar de una situación difícil, incluso traicionar a un amigo"],
        "personality_traits": ["Soy tranquilo bajo presión", "Siempre tengo un plan de escape"],
        "bonds": ["Nunca traiciono a mi grupo, no importa el precio"]
    },
    {
        "name": "Artista",
        "skills": ["Interpretación", "Acrobacias"],
        "languages": [],
        "items": ["Tres instrumentos musicales", "Ropa de actuación", "Tres instrumentos musicales", "Paquete de entretenimiento"],
        "tool_proficiencies": "Tres instrumentos musicales",
        "ideals": ["La creatividad es la más alta forma de expresión (Caótico)", "Quiero hacer el mundo un lugar mejor con mi arte (Bueno)"],
        "flaws": ["Soy un poco arrogante y me encanta ser el centro de atención"],
        "personality_traits": ["Siempre estoy tarareando o cantando", "Tengo un comentario para todo"],
        "bonds": ["Mi arte es mi vida y lo protegeré a toda costa"]
    },
    {
        "name": "Héroe del Pueblo",
        "skills": ["Manejo de Animales", "Supervivencia"],
        "languages": [],
        "items": ["Herramientas de artesano", "Carro", "Paquete de aventurero","Un vehículo terrestre", "Herramientas de artesano"],
        "tool_proficiencies": "Un vehículo terrestre, Herramientas de artesano",
        "ideals": ["La gente común merece ser tratada con dignidad y respeto (Bueno)", "No puedo mirar hacia otro lado cuando alguien está en peligro (Neutral)"],
        "flaws": ["Soy demasiado confiado, lo que a veces me mete en problemas"],
        "personality_traits": ["Trato de ser optimista en todas las situaciones", "Nunca dejo atrás a alguien que necesita ayuda"],
        "bonds": ["Haré cualquier cosa para proteger a mi comunidad"]
    },
    {
        "name": "Artesano del Gremio",
        "skills": ["Persuasión", "Perspicacia"],
        "languages": ["Común"],
        "items": ["Herramientas de artesano", "Carta de presentación", "Herramientas de artesano", "Paquete de gremio"],
        "tool_proficiencies": "Herramientas de artesano",
        "ideals": ["El trabajo duro y la dedicación son lo que construye una comunidad (Legal)", "La estabilidad económica es la clave para una sociedad próspera (Neutral)"],
        "flaws": ["Tengo una aversión extrema hacia los cambios rápidos"],
        "personality_traits": ["Soy extremadamente detallista en mi trabajo", "Valoro la honestidad por encima de todo"],
        "bonds": ["Mi gremio es mi familia y los defenderé hasta el final"]
    },
    {
        "name": "Ermitaño",
        "skills": ["Medicina", "Religión"],
        "languages": ["Común"],
        "items": ["Kit de herbalismo", "Capa", "Kit de herbalismo", "Paquete de ermitaño"],
        "tool_proficiencies": "Kit de herbalismo",
        "ideals": ["La soledad y la meditación son las mejores formas de encontrar la verdad (Neutral)", "Vivo en paz con la naturaleza y todos sus habitantes (Bueno)"],
        "flaws": ["Soy reservado y me cuesta confiar en los demás"],
        "personality_traits": ["Prefiero estar solo que en compañía de otros", "Tengo una gran apreciación por la belleza natural"],
        "bonds": ["Mi retiro espiritual es lo que me mantiene centrado"]
    },
    {
        "name": "Noble",
        "skills": ["Historia", "Persuasión"],
        "languages": ["Común"],
        "items": ["Un tipo de juego", "Ropa fina", "Anillo de sello", "Carta de presentación", "Paquete de noble"],
        "tool_proficiencies": "Un tipo de juego",
        "ideals": ["El poder conlleva responsabilidad, y debo usarlo para proteger a los demás (Legal)", "La nobleza está en el servicio, no en el título (Bueno)"],
        "flaws": ["A menudo subestimo a aquellos que no son de mi estatus"],
        "personality_traits": ["Soy educado y respetuoso con todos", "Me esfuerzo por mantener una apariencia impecable"],
        "bonds": ["Proteger el legado de mi familia es lo más importante para mí"]
    },
    {
        "name": "Forastero",
        "skills": ["Atletismo", "Supervivencia"],
        "languages": ["Común"],
        "items": ["Un bastón", "Un trofeo", "Paquete de aventurero"],
        "tool_proficiencies": "Un Instrumentos Musicales",
        "ideals": ["La libertad es lo más preciado que tenemos (Caótico)", "Debemos preservar el equilibrio de la naturaleza (Neutral)"],
        "flaws": ["Soy desconfiado con aquellos que no conozco bien"],
        "personality_traits": ["Soy extremadamente autosuficiente", "Prefiero la compañía de animales que la de personas"],
        "bonds": ["Tengo una conexión especial con la naturaleza que me guía"]
    },
    {
        "name": "Sabio",
        "skills": ["Arcano", "Historia"],
        "languages": ["Común", "Élfico"],
        "items": ["Un Instrumentos Musicales", "Botella de tinta", "Pluma", "Cuchillo pequeño", "Paquete de erudito"],
        "tool_proficiencies": "",
        "ideals": ["El conocimiento es el camino hacia la comprensión del mundo (Neutral)", "El saber no debe ser oculto, sino compartido para el bien de todos (Bueno)"],
        "flaws": ["Puedo ser arrogante en mi intelecto, menospreciando a los demás"],
        "personality_traits": ["Tengo una sed insaciable de conocimiento", "Soy meticuloso en todo lo que hago"],
        "bonds": ["Mi búsqueda de conocimiento es lo que me define"]
    },
    {
        "name": "Marinero",
        "skills": ["Atletismo", "Percepción"],
        "languages": [],
        "items": ["Vehículo de agua", "Palo corto", "50 pies de cuerda de cáñamo", "Paquete de marinero"],
        "tool_proficiencies": "Vehículo de agua",
        "ideals": ["El mar es libertad, y yo soy libre en él (Caótico)", "La lealtad a mi tripulación es lo primero (Neutral)"],
        "flaws": ["Tengo una debilidad por la bebida"],
        "personality_traits": ["Tengo un gran respeto por el mar", "Siempre estoy buscando la próxima aventura"],
        "bonds": ["Haré cualquier cosa por mis compañeros marineros"]
    },
    {
        "name": "Soldado",
        "skills": ["Atletismo", "Intimidación"],
        "languages": [],
        "items": ["Insignia de rango", "Un dado", "Paquete de soldado", "Un tipo de juego", "Vehículo terrestre"],
        "tool_proficiencies": "Un tipo de juego, Vehículo terrestre",
        "ideals": ["Vivo y muero por mi deber y mi honor (Legal)", "La disciplina y el deber son lo que nos mantiene unidos (Neutral)"],
        "flaws": ["Tengo dificultades para dejar ir el pasado"],
        "personality_traits": ["Soy muy serio y centrado en mi deber", "Tengo una actitud de 'primero en la batalla'"],
        "bonds": ["Siempre seré leal a mi unidad militar"]
    },
    {
        "name": "Huérfano",
        "skills": ["Sigilo", "Juego de Manos"],
        "languages": [],
        "items": ["Cuchillo pequeño", "Mapa", "Paquete de huérfano", "Desactivación de trampas", "Herramientas de ladrón"],
        "tool_proficiencies": "Desactivación de trampas, Herramientas de ladrón",
        "ideals": ["La supervivencia es lo más importante, sin importar los medios (Caótico)", "Nunca confiaré en nadie excepto en mí mismo (Neutral)"],
        "flaws": ["Soy extremadamente desconfiado"],
        "personality_traits": ["Siempre estoy alerta y preparado para lo peor", "Raramente muestro mis emociones"],
        "bonds": ["Tengo un profundo deseo de venganza contra aquellos que me hicieron daño"]
    }
]


def is_table_empty(session, model):
    return session.query(model).count() == 0

# Poblar la base de datos si las tablas están vacías
def populate_db():
    global armors
    global attributes
    global skills
    global items
    global categories
    global languages
    global races
    global classes

    if is_table_empty(session, Attribute):
        for attribute_data in attributes:
            attribute = Attribute(name=attribute_data["name"])
            session.add(attribute)
        session.commit()

    if is_table_empty(session, Class):
        for class_data in classes:
            class_ = Class(
                name=class_data["name"],
                hit_dice=class_data["hit_dice"],
                max_skills=class_data["max_skills"])
            session.add(class_)
        session.commit()

    if is_table_empty(session, Skill):
        for skill_data in skills:
            attribute = session.query(Attribute).filter_by(name=skill_data["attribute"]).first()
            skill = Skill(name=skill_data["name"], attribute_id=attribute.id)
            session.add(skill)
        session.commit()

    if is_table_empty(session, Language):
        for language_data in languages:
            language = Language(name=language_data["name"])
            session.add(language)
        session.commit()

    # Añadir subrazas como razas independientes en lugar de como subrazas
    if is_table_empty(session, Race):
        for race_data in races:
            race = Race(
                name=race_data["name"],
                speed=race_data["speed"],
                extra_strength=race_data["extra_strength"],
                extra_dexterity=race_data["extra_dexterity"],
                extra_constitution=race_data["extra_constitution"],
                extra_intelligence=race_data["extra_intelligence"],
                extra_wisdom=race_data["extra_wisdom"],
                extra_charisma=race_data["extra_charisma"]
            )
            session.add(race)
            session.commit()

            # Asociar idiomas a la raza
            for language_name in race_data["languages"]:
                language = session.query(Language).filter_by(name=language_name).first()
                if language:
                    race.languages.append(language)

            # Asociar habilidades a la raza
            for skill_name in race_data.get("skills", []):
                skill = session.query(Skill).filter_by(name=skill_name).first()
                if skill:
                    race.skills.append(skill)

            # Añadir subrazas como razas independientes
            for subrace_data in race_data.get("subraces", []):
                subrace = Race(
                    name=subrace_data["name"],
                    speed=race_data["speed"],
                    extra_strength=subrace_data.get("extra_strength", race_data["extra_strength"]),
                    extra_dexterity=subrace_data.get("extra_dexterity", race_data["extra_dexterity"]),
                    extra_constitution=subrace_data.get("extra_constitution", race_data["extra_constitution"]),
                    extra_intelligence=subrace_data.get("extra_intelligence", race_data["extra_intelligence"]),
                    extra_wisdom=subrace_data.get("extra_wisdom", race_data["extra_wisdom"]),
                    extra_charisma=subrace_data.get("extra_charisma", race_data["extra_charisma"])
                )
                session.add(subrace)
            session.commit()

    if is_table_empty(session, Category):
        for category_data in categories:
            category = Category(name=category_data["name"])
            session.add(category)
        session.commit()

    if is_table_empty(session, Item):
        for item_data in items:
            category = session.query(Category).filter_by(name=item_data["category"]).first()
            if category is None:
                print(f"Advertencia: La categoría '{item_data['category']}' no se encuentra en la base de datos.")
                continue  # Saltar este ítem si la categoría no existe
            item = Item(
                name=item_data["name"],
                description=item_data["description"],
                category_id=category.id
            )
            session.add(item)
        session.commit()

    if is_table_empty(session, Armor):
        for armor_data in armors:
            armor = Armor(
                name=armor_data["name"],
                armor_class=armor_data["armor_class"],
                type=armor_data["type"],
                strength=armor_data.get("strength"),
                stealth=armor_data.get("stealth"),
                weight=armor_data.get("weight")
            )
            session.add(armor)
        session.commit()

    # Añadir la información a la base de datos
    if is_table_empty(session, Background):
        for background_data in backgrounds:
            # Unir listas de textos en una sola cadena si es necesario
            ideal = ', '.join(background_data.get("ideals", []))
            flaw = ', '.join(background_data.get("flaws", []))
            personality_trait = ', '.join(background_data.get("personality_traits", []))
            bond = ', '.join(background_data.get("bonds", []))

            # Crear la instancia de Background
            background = Background(
                name=background_data["name"],
                tool_proficiencies=background_data["tool_proficiencies"],
                ideal=ideal,
                flaw=flaw,
                personality_trait=personality_trait,
                bond=bond
            )
            session.add(background)
            session.commit()

            # Añadir relaciones a otras tablas si es necesario
            for skill_name in background_data["skills"]:
                skill = session.query(Skill).filter_by(name=skill_name).first()
                if skill:
                    background.skills.append(skill)

            for language_name in background_data["languages"]:
                language = session.query(Language).filter_by(name=language_name).first()
                if language:
                    background.languages.append(language)

            for item_name in background_data["items"]:
                item = session.query(Item).filter_by(name=item_name).first()
                if item:
                    background.items.append(item)

            session.commit()

    # Associations for Class
    # Associations for Class
    for class_data in classes:
        class_ = session.query(Class).filter_by(name=class_data["name"]).first()

        # Asociar habilidades
        for skill_name in class_data["skills"]:
            skill = session.query(Skill).filter_by(name=skill_name).first()
            if skill:
                class_.skills.append(skill)

        # Asociar tiradas de salvación (saving throws)
        for attribute_name in class_data["saving_throws"]:
            attribute = session.query(Attribute).filter_by(name=attribute_name).first()
            if attribute:
                class_.saving_throws.append(attribute)  # Agregar esto para asociar los atributos

        # Asociar items y armaduras
        for item_name in class_data["items"]:
            item = session.query(Item).filter_by(name=item_name).first()
            if item:
                class_.items.append(item)
        for armor_type in class_data["armor"]:
            if armor_type == "Todas las armaduras":
                armors = session.query(Armor).all()
            else:
                armors = session.query(Armor).filter_by(type=armor_type).all()
            for armor in armors:
                class_.armors.append(armor)

        session.add(class_)
    session.commit()


if __name__ == "__main__":
    populate_db()
