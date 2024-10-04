import sqlite3
from sqlalchemy.orm import sessionmaker
from models import Race, Class, Skill, Background, Category, Attribute
from db import engine


def get_races():
    Session = sessionmaker(bind=engine)
    session = Session()
    races = session.query(Race).all()
    session.close()
    return {
        race.name: {
            'Fuerza': race.extra_strength,
            'Destreza': race.extra_dexterity,
            'Constitución': race.extra_constitution,
            'Inteligencia': race.extra_intelligence,
            'Sabiduría': race.extra_wisdom,
            'Carisma': race.extra_charisma,
            'Velocidad': race.speed}
        for race in races
    }


def get_backgrounds():
    Session = sessionmaker(bind=engine)
    session = Session()
    backgrounds = session.query(Background).all()
    session.close()
    return {
        background.name: {
            'Manejo de herramientas': background.tool_proficiencies,
            'Ideal': background.ideal,
            'Defecto': background.flaw,
            'Rasgos de personalidad': background.personality_trait,
            'Vínculo': background.bond
            }
        for background in backgrounds}


def get_classes(class_name=None):
    Session = sessionmaker(bind=engine)
    session = Session()

    if class_name:
        class_obj = session.query(Class).filter_by(name=class_name).first()
        if class_obj:
            result = {'Hit dice': class_obj.hit_dice}
        else:
            result = None
    else:
        classes = session.query(Class).all()
        result = {
            c.name: {
                'Hit dice': c.hit_dice
            }
            for c in classes
        }

    session.close()
    return result


def get_skills():
    Session = sessionmaker(bind=engine)
    session = Session()
    skills = session.query(Skill).all()
    skills_with_attributes = {skill.name: skill.attribute.name for skill in skills}
    session.close()
    return skills_with_attributes


def get_class_armors(class_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar la clase por nombre
    class_obj = session.query(Class).filter_by(name=class_name).first()

    if class_obj:
        # Obtener las armaduras asociadas a la clase
        armors = [armor.name for armor in class_obj.armors]
    else:
        armors = []

    session.close()

    return armors


def get_race_languages(race_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    race_object = session.query(Race).filter_by(name=race_name).first()

    if race_object:
        languages = [language.name for language in race_object.languages]
    else:
        languages = []

    session.close()
    return languages


def get_background_languages(background_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    # Buscar la clase por nombre
    b_object = session.query(Background).filter_by(name=background_name).first()
    if b_object:
        languages = [language.name for language in b_object.languages]
    else:
        languages = []

    session.close()
    return languages


def get_armor_class(armor_name):
    db_characters = 'database/characters.db'
    query = 'SELECT armor_class FROM armors WHERE name = ?'
    with sqlite3.connect(db_characters) as con:
        cursor = con.cursor()
        cursor.execute(query, (armor_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


def get_class_skills(class_name):
    # Crear una sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar la clase por nombre
    class_obj = session.query(Class).filter_by(name=class_name).first()

    # Si la clase existe, obtener las habilidades asociadas
    if class_obj:
        skills = [skill.name for skill in class_obj.skills]
    else:
        skills = []

    # Cerrar la sesión
    session.close()

    return skills


def get_class_max_skills(class_name):
        db_path = 'database/characters.db'  # Asegúrate de que esta ruta sea la correcta

        query = 'SELECT max_skills FROM classes WHERE name = ?'
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            result = cursor.execute(query, (class_name,)).fetchone()

            if result:
                return result[0]


def get_class_items(class_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    c_object = session.query(Class).filter_by(name=class_name).first()

    if c_object:
        items = [item.name for item in c_object.items]
    else:
        items = []

    session.close()
    return items


def get_background_items(background_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    b_object = session.query(Background).filter_by(name=background_name).first()
    if b_object:
        items = [item.name for item in b_object.items]
    else:
        items = []

    session.close()
    return items


def get_categories():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()
    session.close()
    return [category.name for category in categories]


def get_attributes():
    Session = sessionmaker(bind=engine)
    session = Session()
    attributes = session.query(Attribute).all()
    return attributes


def get_saving_throws(class_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    c_class = session.query(Class).filter_by(name=class_name).first()
    if c_class:
        saving_throws = [saving_throw.name for saving_throw in c_class.saving_throws]
    else:
        saving_throws = []
    session.close()
    return saving_throws