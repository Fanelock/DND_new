from DND_weapons.weapon_files import Shortsword, Dagger, Greatsword, Longbow, Longsword, Glaive, Flintlock, CrossbowLight, \
                                        CrossbowHeavy, Flail, Warhammer, Javelin
from DND_weapons.spell_files import SpellAttack, SpellSave
from DND_weapons.class_files import Rogue, Ranger, Cleric, Fighter, Sorcerer, Gloomstalker, Paladin, Vengeance, Warlock
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

"""

Fane = Gloomstalker(3,"GWF", 3, 2, 3, 1, 3, 2, 2, 3, 13)

Fane_Greatsword = Greatsword(Fane)

hit_counter = 0
total_damage = 0

# Perform 1000 attacks
for i in range(1000):
    hit, roll, damage = Fane_Greatsword.perform_attack(
        ac=15,
        dex=False,
        advantage=False,
        disadvantage=False,
        mastery=True,
        fighting_style=Fane.fighting_style,
        hunters_mark=True
    )
    total_damage += damage
    if hit:
        hit_counter += 1

# Calculate average damage
average_damage = total_damage / 1000

# Print results
print(f"Total Hits: {hit_counter}")
print(f"Total Damage: {total_damage}")
print(f"Average Damage: {average_damage}")


Sorcerer = Sorcerer("name", "type", None, 1, 1, 2, 2, 2, 4, 2, 4, 14)

spell_save = SpellSave(Sorcerer)

save_bonus = 5  # Target's save bonus
dice_number = 2  # Number of damage dice
dice_type = 6  # Type of damage dice
advantage = False  # No advantage
disadvantage = False  # No disadvantage
half_dmg = True  # Target takes half damage on a successful save

# Perform the spell save attack
hit, roll, damage = spell_save.perform_attack(
    save_bonus=save_bonus,
    dice_number=dice_number,
    dice_type=dice_type,
    advantage=advantage,
    disadvantage=disadvantage,
    half_dmg=half_dmg
)

print(f"Hit: {hit}")
print(f"Roll: {roll}")
print(f"Damage: {damage}")

"""

#start_time = time.time()

class DND_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DND Attack and Spell Simulation")

        # Initialize variables
        self.create = Create()
        self.character = None
        self.weapon = None
        self.spell = None

        # Buttons for importing and loading
        self.create_button = tk.Button(master, text="Import Excel File", command=self.import_excel)
        self.create_button.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Saved Characters", command=self.load_saved_characters)
        self.load_button.pack(pady=10)

        # Frame for displaying characters
        self.character_frame = tk.LabelFrame(master, text="Loaded Characters")
        self.character_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.character_listbox = tk.Listbox(self.character_frame)
        self.character_listbox.pack(fill="both", expand=True, padx=10, pady=10)

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
            selection_frame, self.weapon_var, "None", "Greatsword", "Shortsword", "Longsword", "Glaive", "Flail", "Warhammer")
        self.weapon_dropdown.grid(row=1, column=1, padx=10, pady=5)

        self.weapon_ranged_label = tk.Label(selection_frame, text="Ranged Weapons:")
        self.weapon_ranged_label.grid(row=0, column=2, padx=10, pady=5)

        self.weapon_ranged_var = tk.StringVar(value="None")
        self.weapon_ranged_dropdown = tk.OptionMenu(
            selection_frame, self.weapon_ranged_var, "None", "Longbow", "Flintlock",
            "Light Crossbow", "Heavy Crossbow")
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

    def update_character_list(self):
        self.character_listbox.delete(0, tk.END)
        for name in self.create.characters:
            self.character_listbox.insert(tk.END, name)

        if self.create.characters:
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)

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

        if self.pact_weapon_var.get():
            self.character.str = self.character.cha

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
            "Javelin": lambda owner: Javelin(owner, bonus)
        }

        # Initialize the selected weapon
        if weapon_name in weapon_mapping:
            self.weapon = weapon_mapping[weapon_name](self.character)
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

        damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage = self.weapon.simulate_attacks(
            num_attacks=10000, ac=ac, dex=dex, advantage=advantage, disadvantage=disadvantage, mastery = mastery,
            include_crits=include_crits, sneak_attack = sneak_attack, hunters_mark=hunters_mark, bonus=bonus, smite=smite
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
        )
        self.display_results(damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage)

    def display_results(self, damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage):
        result_window = tk.Toplevel(self.master)
        result_window.title("Simulation Results")

        result_text = (
            f"Average Damage: {round(avg_damage, 1)} (Includes Hit Probability)\n"
            f"Average Damage on Hit: {round(avg_hit_damage, 1)} (Excludes Hit Probability)\n"
            f"Number of Hits: {hit_count}\n"
            f"Total Hit Damage: {total_hit_damage}"
        )
        tk.Label(result_window, text=result_text, padx=10, pady=10).pack()

        self.plot_damage_distribution(damage_results)

    def plot_damage_distribution(self, damage_results):
        if not damage_results:
            messagebox.showerror("Error", "No damage results to plot.")
            return

        plt.hist(damage_results, bins=10, alpha=0.75, color='purple')
        plt.title("Damage Distribution")
        plt.xlabel("Damage")
        plt.ylabel("Frequency")
        plt.show()

def run_gui():
    root = tk.Tk()
    app = DND_GUI(root)
    root.mainloop()

    #end_time = time.time()
    #elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    #print(f"GUI Startup Time: {elapsed_time_ms:.2f} ms")

if __name__ == "__main__":
    run_gui()

