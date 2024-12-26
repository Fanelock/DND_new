import pandas as pd
import json
import os
from DND_weapons.class_files import Ranger, Rogue, Sorcerer, Cleric, Fighter

class Create:
    def __init__(self, file=None):
        self.file = file
        self.characters = {}
        self.save_file = "saved_characters.json"  # File to save character data
        self.load_characters()  # Load saved characters on initialization

    def read(self):
        data = pd.read_excel(self.file)

        data['Spell_mod'] = data['Spell_mod'].fillna(0).astype(int)
        data['Spell_DC'] = data['Spell_DC'].fillna(0).astype(int)

        for _, row in data.iterrows():
            name = row['Name']
            level = int(row['Level'])
            class_name = row['Class']
            subclass_name = row.get('Subclass', None)  # Subclass might be optional
            fighting_style = row.get('Fighting Style', None)
            str_mod = int(row['Str'])
            dex_mod = int(row['Dex'])
            con_mod = int(row['Con'])
            int_mod = int(row['Int'])
            wis_mod = int(row['Wis'])
            cha_mod = int(row['Cha'])
            prof_bonus = int(row['Prof'])
            spell_mod = int(row.get('Spell_mod', 0))
            spell_DC = int(row.get('Spell_DC', 0))

            class_ = globals().get(class_name)
            if class_:
                try:
                    if class_name == "Ranger":
                        character = class_(
                            level, subclass_name, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus, spell_mod, spell_DC
                        )
                    elif class_name == "Rogue":
                        character = class_(
                            level, subclass_name, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus, spell_mod, spell_DC
                        )
                    elif class_name == "Cleric":
                        character = class_(
                            level, subclass_name, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus, spell_mod, spell_DC
                        )
                    elif class_name == "Fighter":
                        character = class_(
                            level, subclass_name, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus, spell_mod, spell_DC
                        )
                    elif class_name == "Sorcerer":
                        character = class_(
                            level, subclass_name, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                            prof_bonus, spell_mod, spell_DC
                        )
                    else:
                        print(f"Unsupported class: {class_name}")
                        continue

                    character.name = name
                    self.characters[name] = character
                except TypeError as e:
                    print(f"Error initializing {name}: {e}")
            else:
                print(f"Class {class_name} not found for {name}!")

        self.save_characters()  # Save characters to file after loading

    def save_characters(self):
        with open(self.save_file, "w") as f:
            json.dump(
                {name: character.to_dict() for name, character in self.characters.items()}, f
            )

    def load_characters(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    for name, char_data in data.items():
                        if char_data["class_name"] == "Rogue":
                            self.characters[name] = Rogue.from_dict(char_data)
                        elif char_data["class_name"] == "Ranger":
                            self.characters[name] = Ranger.from_dict(char_data)
                        elif char_data["class_name"] == "Fighter":
                            self.characters[name] = Fighter.from_dict(char_data)
                        elif char_data["class_name"] == "Cleric":
                            self.characters[name] = Cleric.from_dict(char_data)
                        elif char_data["class_name"] == "Sorcerer":
                            self.characters[name] = Sorcerer.from_dict(char_data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading characters: {e}. Starting with an empty character list.")

    def get_character(self, name):
        return self.characters.get(name)



