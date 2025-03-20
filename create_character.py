import pandas as pd
import pickle
import os
from DND_weapons.class_files import Ranger, Rogue, Sorcerer, Cleric, Fighter, Gloomstalker, Paladin, Warlock, Druid, Vengeance

class Create:
    def __init__(self, file=None):
        self.file = file
        self.characters = {}
        self.save_file = "saved_characters.pkl"
        self.load_characters()

    def read(self):
        data = pd.read_excel(self.file)

        data['Spell_mod'] = data['Spell_mod'].fillna(0).astype(str)
        data['Spell_DC'] = data['Spell_DC'].fillna(0).astype(str)

        for _, row in data.iterrows():
            name = row['Name']
            classes = str(row['Class']).split(',') if pd.notna(row['Class']) else []
            subclasses = str(row['Subclass']).split(',') if pd.notna(row['Subclass']) else []
            fighting_style = row.get('Fighting Style', None)
            str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod = (
                int(row['Str']), int(row['Dex']), int(row['Con']),
                int(row['Int']), int(row['Wis']), int(row['Cha'])
            )
            prof_bonus = int(row['Prof'])

            spell_mods = [int(float(mod)) if pd.notna(mod) else 0 for mod in str(row.get('Spell_mod', '')).split(',')]
            spell_dcs = [int(float(dc)) if pd.notna(dc) else 0 for dc in str(row.get('Spell_dc', '')).split(',')]

            character_classes = []

            for i, class_info in enumerate(classes):
                class_name, level = class_info.strip().split(':')  # FIX: Use `level` instead of `class_level`
                level = int(level)
                subclass_name = subclasses[i] if i < len(subclasses) else None

                class_ = globals().get(class_name)
                if class_:
                    try:
                        character = class_(
                            level,  # FIX: Pass `level`
                            subclass_name,
                            fighting_style if i == 0 else None,  # Only first class gets the fighting style
                            str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus,
                            spell_mods[i] if i < len(spell_mods) else 0,
                            spell_dcs[i] if i < len(spell_dcs) else 0
                        )
                        character_classes.append(character)
                    except TypeError as e:
                        print(f"Error initializing {name} ({class_name}): {e}")
                else:
                    print(f"Class {class_name} not found for {name}!")

            self.characters[name] = character_classes  # Store list of class instances

        self.save_characters()

    def save_characters(self):
        with open(self.save_file, "wb") as f:
            pickle.dump(self.characters, f)

    def load_characters(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "rb") as f:
                    self.characters = pickle.load(f)
            except (pickle.PickleError, EOFError) as e:
                print(f"Error loading characters: {e}. Starting with an empty character list.")
                self.characters = {}

    def get_character(self, name):
        return self.characters.get(name)

    def delete_character(self, name):
        if name in self.characters:
            del self.characters[name]
            self.save_characters()
            return True
        return False