from DND_weapons.weapon_files import Shortsword, Dagger, Greatsword, Longbow, Longsword, Glaive, Flintlock
from DND_weapons.class_files import Rogue, Ranger, Cleric, Fighter, Sorcerer
from DND_weapons.Attack import AttackHandler
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

#lol

class DND_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DND Attack Simulation")

        # Initialize Create instance
        self.create = Create()
        self.character = None
        self.weapon = None

        # Buttons for importing and loading
        self.create_button = tk.Button(master, text="Import Excel File", command=self.import_excel)
        self.create_button.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Saved Characters", command=self.load_saved_characters)
        self.load_button.pack(pady=10)

        # Frame for displaying characters
        self.character_frame = tk.LabelFrame(master, text="Loaded Characters")
        self.character_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Character list
        self.character_listbox = tk.Listbox(self.character_frame)
        self.character_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Weapon selection
        self.weapon_label = tk.Label(master, text="Select Weapon:")
        self.weapon_label.pack(pady=5)

        self.weapon_var = tk.StringVar()
        self.weapon_dropdown = tk.OptionMenu(
            master, self.weapon_var, "Greatsword", "Shortsword", "Dagger", "Longbow", "Longsword", "Glaive", "Flintlock"
        )
        self.weapon_dropdown.pack(pady=5)

        # Simulation parameters
        self.ac_label = tk.Label(master, text="Target AC:")
        self.ac_label.pack(pady=5)

        self.ac_entry = tk.Entry(master)
        self.ac_entry.pack(pady=5)

        self.dex_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Use Dexterity", variable=self.dex_var).pack()

        self.advantage_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Advantage", variable=self.advantage_var).pack()

        self.disadvantage_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Disadvantage", variable=self.disadvantage_var).pack()

        self.mastery_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Mastery", variable=self.mastery_var).pack()

        self.include_crits_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Include Critical Hits", variable=self.include_crits_var).pack()

        # Run Simulation Button (enabled after character selection)
        self.run_button = tk.Button(master, text="Run Simulation", state=tk.DISABLED, command=self.run_simulation)
        self.run_button.pack(pady=10)

        # Populate character list at startup
        self.update_character_list()

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            try:
                # Load characters from the Excel file
                self.create.file = file_path
                self.create.read()
                self.update_character_list()
                messagebox.showinfo("Success", "Characters imported and saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import characters: {str(e)}")

    def load_saved_characters(self):
        """Load saved characters from the JSON file."""
        try:
            self.create.load_characters()
            self.update_character_list()
            messagebox.showinfo("Success", "Saved characters loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved characters: {str(e)}")

    def update_character_list(self):
        """Update the character listbox with the current characters."""
        self.character_listbox.delete(0, tk.END)
        for name in self.create.characters:
            self.character_listbox.insert(tk.END, name)

        # Enable the Run Simulation button if characters exist
        if self.create.characters:
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)

    def run_simulation(self):
        try:
            # Retrieve selected character
            selected_index = self.character_listbox.curselection()
            if not selected_index:
                raise ValueError("Please select a character.")

            character_name = self.character_listbox.get(selected_index)
            self.character = self.create.get_character(character_name)

            # Retrieve selected weapon
            weapon_name = self.weapon_var.get()
            if not weapon_name:
                raise ValueError("Please select a weapon.")

            weapon_mapping = {
                "Greatsword": Greatsword,
                "Shortsword": Shortsword,
                "Dagger": Dagger,
                "Longbow": Longbow,
                "Longsword": Longsword,
                "Glaive": Glaive,
                "Flintlock": Flintlock
            }
            self.weapon = weapon_mapping.get(weapon_name)(self.character)

            # Retrieve attack inputs
            ac = int(self.ac_entry.get())
            dex = self.dex_var.get()
            advantage = self.advantage_var.get()
            disadvantage = self.disadvantage_var.get()
            mastery = self.mastery_var.get()
            include_crits = self.include_crits_var.get()

            # Run the simulation
            damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage = self.weapon.simulate_attacks(
                num_attacks=1000,
                ac=ac,
                dex=dex,
                advantage=advantage,
                disadvantage=disadvantage,
                mastery=mastery,
                include_crits=include_crits
            )

            self.display_results(damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def display_results(self, damage_results, avg_damage, avg_hit_damage, hit_count, total_hit_damage):
        """Display the results of the simulation."""
        result_window = tk.Toplevel(self.master)
        result_window.title("Simulation Results")

        result_text = (
            f"Average Damage: {round(avg_damage, 2)}\n"
            f"Average Damage on Hit: {round(avg_hit_damage, 2)}\n"
            f"Total Hits: {hit_count}\n"
            f"Total Hit Damage: {total_hit_damage}"
        )
        tk.Label(result_window, text=result_text, padx=10, pady=10).pack()

        # Plot damage distribution
        self.plot_damage_distribution(damage_results)

    def plot_damage_distribution(self, damage_results):
        """Plot the damage distribution."""
        if not damage_results:
            messagebox.showerror("Error", "No damage results to plot.")
            return

        plt.hist(damage_results, bins=10, alpha=0.75, color='blue')
        plt.title("Damage Distribution")
        plt.xlabel("Damage")
        plt.ylabel("Frequency")
        plt.show()


def run_gui():
    root = tk.Tk()
    app = DND_GUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()