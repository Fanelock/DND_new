import pandas as pd
import pickle
import os
from DND_weapons.class_files import Ranger, Rogue, Sorcerer, Cleric, Fighter, Gloomstalker, Paladin, Warlock, Druid, Vengeance

class Create:
    def __init__(self, file=None):
        self.file = file
        self.characters = {}
        self.save_file = "saved_characters.pkl"  # Use pickle for saving class instances
        self.load_characters()  # Load saved characters on initialization

    def read(self):
        data = pd.read_excel(self.file)

        data['Spell_mod'] = data['Spell_mod'].fillna(0).astype(str)
        data['Spell_DC'] = data['Spell_DC'].fillna(0).astype(str)

        for _, row in data.iterrows():
            name = row['Name']
            classes = str(row['Class']).split(',') if pd.notna(row['Class']) else []
            subclasses = [None] if pd.isna(row.get('Subclass', None)) else str(row['Subclass']).split(',')
            fighting_style = row.get('Fighting Style', None)
            str_mod = int(row['Str'])
            dex_mod = int(row['Dex'])
            con_mod = int(row['Con'])
            int_mod = int(row['Int'])
            wis_mod = int(row['Wis'])
            cha_mod = int(row['Cha'])
            prof_bonus = int(row['Prof'])

            spell_mods = [int(float(mod)) if pd.notna(mod) else None for mod in
                        str(row.get('Spell_mod', '')).split(',')]
            spell_DCs = [int(float(dc)) if pd.notna(dc) else None for dc in str(row.get('Spell_DC', '')).split(',')]

            character_classes = []

            for i, class_info in enumerate(classes):
                class_name, class_level = class_info.split(':')
                class_level = int(class_level)
                subclass_name = subclasses[i] if i < len(subclasses) and subclasses[i] else None
                class_ = globals().get(class_name)

                if class_:
                    try:
                        character = class_(
                            class_level,
                            subclass_name,
                            fighting_style,
                            str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus,
                            int(spell_mods[i]) if i < len(spell_mods) else 0,
                            int(spell_DCs[i]) if i < len(spell_DCs) else 0
                        )
                        character_classes.append(character)
                    except TypeError as e:
                        print(f"Error initializing {name} ({class_name}): {e}")
                else:
                    print(f"Class {class_name} not found for {name}!")

            self.characters[name] = character_classes  # Store the list of class instances directly

        self.save_characters()  # Save characters to file after loading

    def save_characters(self):
        with open(self.save_file, "wb") as f:
            pickle.dump(self.characters, f)  # Save the entire dictionary of class instances

    def load_characters(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "rb") as f:
                    self.characters = pickle.load(f)  # Load class instances directly
            except (pickle.PickleError, EOFError) as e:
                print(f"Error loading characters: {e}. Starting with an empty character list.")
                self.characters = {}

    def get_character(self, name):
        return self.characters.get(name)