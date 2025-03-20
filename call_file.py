from DND_weapons import Shortbow
from DND_weapons.weapon_files import Shortsword, Dagger, Greatsword, Longbow, Longsword, Glaive, Flintlock, CrossbowLight, \
                                        CrossbowHeavy, Flail, Warhammer, Javelin, Rapier, Shortbow
from DND_weapons.spell_files import SpellAttack, SpellSave
from DND_weapons.class_files import Rogue, Ranger, Cleric, Fighter, Sorcerer, Gloomstalker, Paladin, Vengeance, Warlock, Druid
from DND_weapons.Attack import AttackHandler
from DND_weapons.SpellAttack import SpellAttackHandler
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
import math
import random as rd
from DND_weapons.create_character import Create
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import time

#start_time = time.time()

class DND_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DND Attack and Spell Simulation")
        self.master.geometry("550x650+50+50")

        # Initialize variables
        self.create = Create()
        self.character = None
        self.weapon = None
        self.spell = None

        # Buttons for importing and loading

        selection_frame = tk.Frame(master)
        selection_frame.pack(pady=10)

        selection_frame.grid_rowconfigure(0, weight=1)
        selection_frame.grid_rowconfigure(1, weight=1)
        selection_frame.grid_columnconfigure(0, weight=1)
        selection_frame.grid_columnconfigure(1, weight=1)
        selection_frame.grid_columnconfigure(2, weight=1)

        self.create_button = tk.Button(selection_frame, text="Create New Character", command=self.create_character)
        self.create_button.grid(row=0, column=0, padx=10, pady=5)

        self.load_button = tk.Button(selection_frame, text="Load Characters", command=self.load_saved_characters)
        self.load_button.grid(row=0, column=1, padx=10, pady=5)

        self.edit_button = tk.Button(selection_frame, text="Edit Character", command=self.edit_character)
        self.edit_button.grid(row=0, column=2, padx=10, pady=5)

        self.delete_button = tk.Button(selection_frame, text="Delete Character", command=self.delete_character)
        self.delete_button.grid(row=0, column=3, padx=10, pady=5)

        # Frame for displaying characters
        self.character_frame = tk.LabelFrame(master, text="Loaded Characters")
        self.character_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.character_listbox = tk.Listbox(self.character_frame, height=8)
        self.character_scrollbar = tk.Scrollbar(self.character_frame, orient=tk.VERTICAL)

        self.character_listbox.config(yscrollcommand=self.character_scrollbar.set)
        self.character_scrollbar.config(command=self.character_listbox.yview)

        self.character_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
        self.character_scrollbar.pack(side=tk.RIGHT, fill="y")

        # Weapon and spell selection
        selection_frame = tk.Frame(master)
        selection_frame.pack(pady=10)

        selection_frame.grid_rowconfigure(0, weight=1)
        selection_frame.grid_rowconfigure(1, weight=1)
        selection_frame.grid_rowconfigure(2, weight=1)
        selection_frame.grid_rowconfigure(3, weight=1)
        selection_frame.grid_rowconfigure(4, weight=1)
        selection_frame.grid_columnconfigure(0, weight=1)
        selection_frame.grid_columnconfigure(1, weight=1)
        selection_frame.grid_columnconfigure(2, weight=1)
        selection_frame.grid_columnconfigure(3, weight=1)
        selection_frame.grid_columnconfigure(4, weight=1)

        self.weapon_simple_label = tk.Label(selection_frame, text="Simple Melee Weapons:")
        self.weapon_simple_label.grid(row=0, column=0, padx=10, pady=5)

        self.weapon_simple_var = tk.StringVar(value="None")
        self.weapon_simple_dropdown = tk.OptionMenu(
            selection_frame, self.weapon_simple_var, "None", "Dagger", "Javelin")
        self.weapon_simple_dropdown.grid(row=1, column=0, padx=10, pady=5)

        self.weapon_label = tk.Label(selection_frame, text="Martial Melee Weapons:")
        self.weapon_label.grid(row=0, column=1, padx=10, pady=5)

        self.weapon_var = tk.StringVar(value="None")
        self.weapon_dropdown = tk.OptionMenu(
            selection_frame, self.weapon_var, "None", "Greatsword", "Shortsword", "Longsword", "Glaive", "Flail", "Warhammer", "Rapier")
        self.weapon_dropdown.grid(row=1, column=1, padx=10, pady=5)

        self.weapon_ranged_label = tk.Label(selection_frame, text="Ranged Weapons:")
        self.weapon_ranged_label.grid(row=0, column=2, padx=10, pady=5)

        self.weapon_ranged_var = tk.StringVar(value="None")
        self.weapon_ranged_dropdown = tk.OptionMenu(
            selection_frame, self.weapon_ranged_var, "None", "Shortbow", "Longbow",
            "Light Crossbow", "Heavy Crossbow", "Flintlock")
        self.weapon_ranged_dropdown.grid(row=1, column=2, padx=10, pady=5)

        self.spell_label = tk.Label(selection_frame, text="Select Spell:")
        self.spell_label.grid(row=0, column=3, padx=10, pady=5)

        self.spell_var = tk.StringVar(value="None")
        self.spell_dropdown = tk.OptionMenu(selection_frame, self.spell_var, "None", "SpellAttack", "SpellSave")
        self.spell_dropdown.grid(row=1, column=3, padx=10, pady=5)

        # Parameters frame
        parameters_frame = tk.Frame(master)
        parameters_frame.pack(pady=10)

        self.ac_label = tk.Label(parameters_frame, text="Target AC:")
        self.ac_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ac_entry = tk.Entry(parameters_frame)
        self.ac_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.dex_var = tk.BooleanVar()
        self.dex_checkbox = tk.Checkbutton(parameters_frame, text="Use Dexterity", variable=self.dex_var)
        self.dex_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.advantage_var = tk.BooleanVar()
        self.advantage_checkbox = tk.Checkbutton(parameters_frame, text="Advantage", variable=self.advantage_var)
        self.advantage_checkbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.disadvantage_var = tk.BooleanVar()
        self.disadvantage_checkbox = tk.Checkbutton(parameters_frame, text="Disadvantage", variable=self.disadvantage_var)
        self.disadvantage_checkbox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.mastery_var = tk.BooleanVar()  # Variable to hold the state of the checkbox
        self.mastery_checkbox = tk.Checkbutton(parameters_frame, text="Mastery", variable=self.mastery_var)
        self.mastery_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.hunters_mark_var = tk.BooleanVar()
        self.hunters_mark_checkbox = tk.Checkbutton(parameters_frame, text="Hunters Mark", variable=self.hunters_mark_var)
        self.hunters_mark_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.sneak_attack_var = tk.BooleanVar()
        self.sneak_attack_checkbox = tk.Checkbutton(parameters_frame, text="Sneak Attack", variable=self.sneak_attack_var)
        self.sneak_attack_checkbox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.smite_var = tk.BooleanVar()
        self.smite_checkbox = tk.Checkbutton(parameters_frame, text="Smite", variable=self.smite_var)
        self.smite_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.plus_one_var = tk.BooleanVar()
        self.plus_one_checkbox = tk.Checkbutton(parameters_frame, text="+1 Item", variable=self.plus_one_var)
        self.plus_one_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.dice_number_label = tk.Label(parameters_frame, text="Dice Number:")
        self.dice_number_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.dice_number_entry = tk.Entry(parameters_frame)
        self.dice_number_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        self.dice_type_label = tk.Label(parameters_frame, text="Dice Type:")
        self.dice_type_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.dice_type_entry = tk.Entry(parameters_frame)
        self.dice_type_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        self.save_label = tk.Label(parameters_frame, text="Target Save Bonus:")
        self.save_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.save_entry = tk.Entry(parameters_frame)
        self.save_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        self.half_dmg_var = tk.BooleanVar()
        self.half_dmg_checkbox = tk.Checkbutton(parameters_frame, text="Half Damage", variable=self.half_dmg_var)
        self.half_dmg_checkbox.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.include_crits_var = tk.BooleanVar()
        self.include_crits_checkbox = tk.Checkbutton(parameters_frame, text="Include Critical Hits", variable=self.include_crits_var)
        self.include_crits_checkbox.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        self.plus_two_var = tk.BooleanVar()
        self.plus_two_checkbox = tk.Checkbutton(parameters_frame, text="+2 Item", variable=self.plus_two_var)
        self.plus_two_checkbox.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.plus_three_var = tk.BooleanVar()
        self.plus_three_checkbox = tk.Checkbutton(parameters_frame, text="+3 Item", variable=self.plus_three_var)
        self.plus_three_checkbox.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        self.pact_weapon_var = tk.BooleanVar()
        self.pact_weapon_checkbox = tk.Checkbutton(parameters_frame, text="Pact Weapon", variable=self.pact_weapon_var)
        self.pact_weapon_checkbox.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.strike_var = tk.BooleanVar()
        self.strike_checkbox = tk.Checkbutton(parameters_frame, text="Primal/Blessed Strike", variable=self.strike_var)
        self.strike_checkbox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.cantrip_mod_var = tk.BooleanVar()
        self.cantrip_mod_checkbox = tk.Checkbutton(parameters_frame, text="Add Spell Mod", variable=self.cantrip_mod_var)
        self.cantrip_mod_checkbox.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Run Simulation Button
        self.run_button = tk.Button(master, text="Run Simulation", state=tk.DISABLED, command=self.run_simulation)
        self.run_button.pack(pady=10)

        self.update_character_list()

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            try:
                self.create.file = file_path
                self.create.read()
                self.update_character_list()
                messagebox.showinfo("Success", "Characters imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import characters: {str(e)}")

    def load_saved_characters(self):
        try:
            self.create.load_characters()
            self.update_character_list()
            messagebox.showinfo("Success", "Saved characters loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved characters: {str(e)}")

    def create_character(self):
        self.create_window = tk.Toplevel(self.master)
        self.create_window.title("Create New Character")
        self.create_window.geometry("400x400")

        tk.Label(self.create_window, text="Character Name:").pack()
        self.new_name_entry = tk.Entry(self.create_window)
        self.new_name_entry.pack(pady=5)

        tk.Label(self.create_window, text="Class (Format: Class:Level)").pack()
        self.new_class_entry = tk.Entry(self.create_window)
        self.new_class_entry.pack(pady=5)

        tk.Label(self.create_window, text="Subclass (Optional)").pack()
        self.new_subclass_entry = tk.Entry(self.create_window)
        self.new_subclass_entry.pack(pady=5)

        tk.Label(self.create_window, text="Fighting Style (Optional)").pack()
        self.new_fighting_style_entry = tk.Entry(self.create_window)
        self.new_fighting_style_entry.pack(pady=5)

        # **3x3 Ability & Bonus Matrix Layout**
        tk.Label(self.create_window, text="Character Attributes").pack()

        matrix_frame = tk.Frame(self.create_window)
        matrix_frame.pack(pady=10)

        attributes = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
        extra_attributes = ['Prof Bonus', 'Spell DC', 'Spell Mod']

        self.ability_entries = {}
        self.extra_entries = {}

        for i, attr in enumerate(attributes):
            row, col = divmod(i, 3)  # 2D Grid Placement (Row, Col)
            tk.Label(matrix_frame, text=f"{attr}:").grid(row=row, column=col * 2, padx=5, pady=2, sticky="w")
            entry = tk.Entry(matrix_frame, width=5)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
            self.ability_entries[attr] = entry

        for i, attr in enumerate(extra_attributes):
            row, col = divmod(i + 6, 3)  # Next row after ability scores
            tk.Label(matrix_frame, text=f"{attr}:").grid(row=row, column=col * 2, padx=5, pady=2, sticky="w")
            entry = tk.Entry(matrix_frame, width=5)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
            self.extra_entries[attr] = entry

        self.save_button = tk.Button(self.create_window, text="Save Character", command=self.save_new_character)
        self.save_button.pack(pady=20)

    def save_new_character(self):
        try:
            name = self.new_name_entry.get().strip()
            class_info = self.new_class_entry.get().strip()
            subclass = self.new_subclass_entry.get().strip() or None
            fighting_style = self.new_fighting_style_entry.get().strip() or None

            abilities = {ability: int(self.ability_entries[ability].get()) for ability in self.ability_entries}

            # Proficiency Bonus (Required)
            prof_bonus_value = self.extra_entries['Prof Bonus'].get().strip()

            if not prof_bonus_value.isdigit():
                messagebox.showerror("Error", "Proficiency Bonus is required and must be a number.")
                return
            prof_bonus = int(prof_bonus_value)

            # Spell DC & Spell Mod (Optional)
            spell_dc_value = self.extra_entries['Spell DC'].get().strip()
            spell_mod_value = self.extra_entries['Spell Mod'].get().strip()

            spell_dc = int(spell_dc_value) if spell_dc_value.isdigit() else None
            spell_mod = int(spell_mod_value) if spell_mod_value.isdigit() else None

            class_name, class_level = class_info.split(':')
            class_level = int(class_level)

            class_ = globals().get(class_name)
            if not class_:
                messagebox.showerror("Error", f"Class '{class_name}' not found.")
                return

            new_character = class_(
                level=class_level,
                subclass=subclass,
                fighting_style=fighting_style,
                str_mod=abilities['Str'], dex_mod=abilities['Dex'], con_mod=abilities['Con'],
                int_mod=abilities['Int'], wis_mod=abilities['Wis'], cha_mod=abilities['Cha'],
                prof_bonus=prof_bonus,  # Required, no default
                spell_mod=spell_mod if spell_mod is not None else 0,  # Optional
                spell_dc=spell_dc if spell_dc is not None else 0  # Optional
            )

            self.create.characters[name] = [new_character]
            self.create.save_characters()
            self.update_character_list()

            messagebox.showinfo("Success", f"Character '{name}' created successfully.")
            self.create_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_character_list(self):
        self.character_listbox.delete(0, tk.END)
        for name in self.create.characters:
            self.character_listbox.insert(tk.END, name)

        if self.create.characters:
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)

    def edit_character(self):
        try:
            selected_character = self.character_listbox.get(self.character_listbox.curselection())
            character = self.create.get_character(selected_character)

            if character:
                self.edit_window = tk.Toplevel(self.master)
                self.edit_window.title(f"Edit {selected_character}")
                self.edit_window.geometry("400x450")

                tk.Label(self.edit_window, text="Character Name:").pack()
                self.name_entry = tk.Entry(self.edit_window)
                self.name_entry.insert(0, selected_character)
                self.name_entry.pack(pady=5)

                tk.Label(self.edit_window, text="Classes (Format: Class:Level,Class:Level):").pack()
                self.class_entry = tk.Entry(self.edit_window)
                self.class_entry.insert(0, ', '.join(
                    [f"{cls.__class__.__name__}:{getattr(cls, 'level', 1)}" for cls in character]))
                self.class_entry.pack(pady=5)

                tk.Label(self.edit_window, text="Subclasses (comma-separated):").pack()
                self.subclass_entry = tk.Entry(self.edit_window)
                subclass_values = [cls.subclass if cls.subclass else '' for cls in character]
                subclass_string = ', '.join(subclass_values) if any(subclass_values) else ''
                self.subclass_entry.insert(0, subclass_string)
                self.subclass_entry.pack(pady=5)

                tk.Label(self.edit_window, text="Fighting Style:").pack()
                self.fighting_style_entry = tk.Entry(self.edit_window)
                fighting_style_value = getattr(character[0], 'fighting_style', '') or ''
                self.fighting_style_entry.insert(0, fighting_style_value)
                self.fighting_style_entry.pack(pady=5)

                tk.Label(self.edit_window, text="Character Attributes").pack()
                matrix_frame = tk.Frame(self.edit_window)
                matrix_frame.pack(pady=10)

                ability_scores = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
                extra_attributes = ['Prof Bonus', 'Spell DC', 'Spell Mod']

                self.ability_entries = {}
                self.extra_entries = {}

                for i, ability in enumerate(ability_scores):
                    row, col = divmod(i, 3)
                    tk.Label(matrix_frame, text=f"{ability}:").grid(row=row, column=col * 2, padx=5, pady=2, sticky="w")
                    entry = tk.Entry(matrix_frame, width=5)
                    ability_value = getattr(character[0], ability.lower(), 0)
                    entry.insert(0, str(ability_value))
                    entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
                    self.ability_entries[ability] = entry

                for i, attr in enumerate(extra_attributes):
                    row, col = divmod(i + 6, 3)
                    tk.Label(matrix_frame, text=f"{attr}:").grid(row=row, column=col * 2, padx=5, pady=2, sticky="w")
                    entry = tk.Entry(matrix_frame, width=5)

                    attr_value = getattr(character[0], attr.lower().replace(' ', '_'), None)

                    if attr == "Prof Bonus":
                        if attr_value is None or attr_value == 0:
                            attr_value = "2"  # Default to 2, but should display correct value if saved
                        else:
                            attr_value = str(attr_value)  # Convert to string before inserting

                    elif attr == "Spell DC":
                        if attr_value is None:
                            attr_value = ""  # Keep empty if not set
                        else:
                            attr_value = str(attr_value)

                    elif attr == "Spell Mod":
                        if attr_value is None:
                            attr_value = ""
                        else:
                            attr_value = str(attr_value)

                    entry.insert(0, str(attr_value))
                    entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
                    self.extra_entries[attr] = entry

                self.save_button = tk.Button(self.edit_window, text="Save Changes", command=self.save_edited_character)
                self.save_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_edited_character(self):
        try:
            new_name = self.name_entry.get().strip()
            new_classes = self.class_entry.get().split(',')
            new_subclasses = self.subclass_entry.get().split(',')
            new_fighting_style = self.fighting_style_entry.get().strip()

            # Parse Ability Scores
            new_abilities = {ability: int(self.ability_entries[ability].get()) for ability in self.ability_entries}

            # Proficiency Bonus (Required)
            prof_bonus_value = self.extra_entries['Prof Bonus'].get().strip()

            if not prof_bonus_value.isdigit():
                messagebox.showerror("Error", "Proficiency Bonus is required and must be a number.")
                return
            prof_bonus = int(prof_bonus_value)

            # Spell DC & Spell Mod (Optional)
            spell_dc_value = self.extra_entries['Spell DC'].get().strip()
            spell_mod_value = self.extra_entries['Spell Mod'].get().strip()

            spell_dc = int(spell_dc_value) if spell_dc_value.isdigit() else None
            spell_mod = int(spell_mod_value) if spell_mod_value.isdigit() else None

            new_character = []
            for i, class_info in enumerate(new_classes):
                class_name, class_level = class_info.strip().split(':')
                class_level = int(class_level)
                subclass_name = new_subclasses[i] if i < len(new_subclasses) else None

                class_ = globals().get(class_name)
                if class_:
                    updated_character = class_(
                        level=class_level,
                        subclass=subclass_name,
                        fighting_style=new_fighting_style if i == 0 else None,
                        str_mod=new_abilities['Str'], dex_mod=new_abilities['Dex'], con_mod=new_abilities['Con'],
                        int_mod=new_abilities['Int'], wis_mod=new_abilities['Wis'], cha_mod=new_abilities['Cha'],
                        prof_bonus=prof_bonus,  # Required, no default
                        spell_mod=spell_mod if spell_mod is not None else 0,  # Optional
                        spell_dc=spell_dc if spell_dc is not None else 0  # Optional
                    )

                    new_character.append(updated_character)
                else:
                    raise ValueError(f"Class {class_name} not found.")

            self.create.characters[new_name] = new_character

            self.create.save_characters()

            self.update_character_list()
            messagebox.showinfo("Success", f"Character '{new_name}' updated successfully.")
            self.edit_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
            print(f"Error saving edited character: {e}")

    def delete_character(self):
        try:
            # Get the selected index from the listbox
            selected_index = self.character_listbox.curselection()

            # Check if an item is selected
            if not selected_index:
                messagebox.showwarning("Warning", "No character selected for deletion.")
                return

            selected_character = self.character_listbox.get(selected_index)

            confirm = messagebox.askyesno("Confirm Deletion",
                                        f"Are you sure you want to delete '{selected_character}'?")
            if not confirm:
                return

            character = self.create.get_character(selected_character)

            if character:
                self.create.delete_character(selected_character)

                self.character_listbox.delete(selected_index)

                messagebox.showinfo("Success", f"Character '{selected_character}' deleted successfully.")
            else:
                messagebox.showerror("Error", "Character not found in data storage.")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def run_simulation(self):
        try:
            selected_character = self.character_listbox.get(self.character_listbox.curselection())
            self.character = self.create.get_character(selected_character)

            weapon_name = next(
                (name for name in [self.weapon_simple_var.get(), self.weapon_var.get(), self.weapon_ranged_var.get()] if
                name != "None"), None
            )
            spell_name = self.spell_var.get()

            if spell_name != "None" and spell_name:
                self.simulate_spell(spell_name)
            elif weapon_name:
                self.simulate_weapon(weapon_name)
            else:
                raise ValueError("Please select a weapon or spell.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def get_bonus(self):
        if self.plus_one_var.get():
            return 1
        elif self.plus_two_var.get():
            return 2
        elif self.plus_three_var.get():
            return 3
        return 0

    def simulate_weapon(self, weapon_name):
        bonus = self.get_bonus()

        class_instance = next((cls for cls in self.character if hasattr(cls, 'fighting_style')), None)

        if not class_instance:
            messagebox.showerror("Error", "No valid class with a fighting style found for the selected character.")
            return

        class_instance = next((cls for cls in self.character if hasattr(cls, 'cha')), None)

        if class_instance:
            if self.pact_weapon_var.get():
                class_instance.str = class_instance.cha

        weapon_mapping = {
            "Greatsword": lambda owner: Greatsword(owner, bonus),
            "Shortsword": lambda owner: Shortsword(owner, bonus),
            "Dagger": lambda owner: Dagger(owner, bonus),
            "Longbow": lambda owner: Longbow(owner, bonus),
            "Longsword": lambda owner: Longsword(owner, bonus),
            "Glaive": lambda owner: Glaive(owner, bonus),
            "Flintlock": lambda owner: Flintlock(owner, bonus),
            "Light Crossbow": lambda owner: CrossbowLight(owner, bonus),
            "Heavy Crossbow": lambda owner: CrossbowHeavy(owner, bonus),
            "Flail": lambda owner: Flail(owner, bonus),
            "Warhammer": lambda owner: Warhammer(owner, bonus),
            "Javelin": lambda owner: Javelin(owner, bonus),
            "Rapier": lambda owner: Rapier(owner, bonus),
            "Shortbow": lambda owner: Shortbow(owner, bonus)
        }

        # Initialize the selected weapon
        if weapon_name in weapon_mapping:
            self.weapon = weapon_mapping[weapon_name](class_instance)
        else:
            raise ValueError(f"Weapon '{weapon_name}' not recognized.")

        ac = int(self.ac_entry.get())
        dex = self.dex_var.get()
        advantage = self.advantage_var.get()
        disadvantage = self.disadvantage_var.get()
        mastery = self.mastery_var.get()
        include_crits = self.include_crits_var.get()
        sneak_attack = self.sneak_attack_var.get()
        hunters_mark = self.hunters_mark_var.get()
        smite = self.smite_var.get()
        strike = self.strike_var.get()

        damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage = self.weapon.simulate_attacks(
            num_attacks=10000,
            ac=ac,
            dex=dex,
            advantage=advantage,
            disadvantage=disadvantage,
            mastery = mastery,
            include_crits=include_crits,
            sneak_attack = sneak_attack,
            hunters_mark=hunters_mark,
            bonus=bonus,
            smite=smite,
            strike = strike
        )

        self.display_results(damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage)

    def simulate_spell(self, spell_name):
        bonus = self.get_bonus()
        spell_mapping = {
            "SpellAttack": lambda owner: SpellAttack(owner, bonus),
            "SpellSave": lambda owner: SpellSave(owner, bonus)}
        self.spell = spell_mapping[spell_name](self.character)

        ac = int(self.ac_entry.get())
        dice_number = int(self.dice_number_entry.get())
        dice_type = int(self.dice_type_entry.get())
        save_bonus = int(self.save_entry.get()) if spell_name == "SpellSave" else None
        half_dmg = self.half_dmg_var.get()
        advantage = self.advantage_var.get()
        disadvantage = self.disadvantage_var.get()
        include_crits = self.include_crits_var.get()
        sneak_attack = self.sneak_attack_var.get()
        hunters_mark = self.hunters_mark_var.get()
        smite = self.smite_var.get()
        cantrip_mod = self.cantrip_mod_var.get()

        damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage = self.spell.simulate_attacks(
            ac=ac,
            save_bonus=save_bonus,
            dice_number=dice_number,
            dice_type=dice_type,
            num_attacks=10000,
            advantage=advantage,
            disadvantage=disadvantage,
            half_dmg=half_dmg,
            include_crits = include_crits,
            sneak_attack = sneak_attack,
            hunters_mark = hunters_mark,
            bonus = bonus,
            smite = smite,
            cantrip_mod = cantrip_mod,
        )
        self.display_results(damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage)

    def display_results(self, damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage):
        result_window = tk.Toplevel(self.master)
        result_window.title("Simulation Results")

        main_x = self.master.winfo_rootx()
        main_y = self.master.winfo_rooty()
        popup_width = 320
        popup_height = 80
        popup_x = main_x + 550  # Offset by 50px horizontally from main window
        popup_y = main_y - 30  # Offset by 50px vertically from main window
        result_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        result_text = (
            f"Average Damage per Turn: {round(avg_damage, 1)}\n"
            f"Average Damage on Hit: {round(avg_hit_damage, 1)}\n" 
            f"Number of Hits: {hit_count}\n"
            f"Total Hit Damage: {total_hit_damage}"
        )
        tk.Label(result_window, text=result_text, padx=10, pady=10).pack()

        self.plot_damage_distribution(damage_results)

    def plot_damage_distribution(self, damage_results):
        if not damage_results:
            messagebox.showerror("Error", "No damage results to plot.")
            return

        # Create the plot
        fig, ax = plt.subplots()
        ax.hist(damage_results, bins=10, alpha=0.75, color='purple')
        ax.set_title("Damage Distribution")
        ax.set_xlabel("Damage")
        ax.set_ylabel("Frequency")

        # Show the plot
        plt.show(block=False)

        # Position the plot window
        try:
            backend = plt.get_current_fig_manager()
            main_x = self.master.winfo_rootx()
            main_y = self.master.winfo_rooty()
            plot_x = main_x + 550  # Offset horizontally
            plot_y = main_y + 100  # Offset vertically

            # TkAgg backend
            if hasattr(backend, "window"):
                backend.window.wm_geometry(f"+{plot_x}+{plot_y}")
            # Other backends (fallback)
            elif hasattr(backend, "canvas"):
                backend.canvas.manager.window.wm_geometry(f"+{plot_x}+{plot_y}")
            else:
                print("Could not reposition the matplotlib window.")
        except Exception as e:
            print(f"Error repositioning plot: {e}")

def run_gui():
    root = tk.Tk()
    app = DND_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()

