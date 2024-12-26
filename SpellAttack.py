from DND_weapons.class_files import Sorcerer, Cleric
from DND_weapons.spell_files import SpellSave
from spell_files.Spell_attack import SpellAttack

class SpellAttackHandler:
    @staticmethod
    def get_attack_inputs():

        inputs = {
            "ac": int(input("Enter the target's AC (Armor Class): ")),
            "dice_Number": int(input("Enter the Spells Dice Number: ")),
            "dice_Type": int(input("Enter the Spells Dice Type: ")),
            "advantage": input("Does the attack have advantage? (1/0): ").strip().lower() == "1",
            "disadvantage": input("Does the attack have disadvantage? (1/0): ").strip().lower() == "1",
        }
        return inputs

    @staticmethod
    def get_save_inputs():

        inputs = {
            "save_bonus": int(input("Enter the target's save bonus: ")),
            "half_dmg": input("Does a save deal half damage? (1/0): ").strip().lower() == "1",
            "dice_Number": int(input("Enter the Spells Dice Number: ")),
            "dice_Type": int(input("Enter the Spells Dice Type: ")),
            "advantage": input("Does the target have advantage? (1/0): ").strip().lower() == "1",
            "disadvantage": input("Does the target have disadvantage? (1/0): ").strip().lower() == "1",}
        return inputs

    @staticmethod
    def perform_attack(spell, owner):
        print(f"Attacking with spell...")

        # Collect user inputs
        attack_inputs = SpellAttackHandler.get_attack_inputs()

        damage = spell.perform_attack(
            **attack_inputs
        )

        return damage

    @staticmethod
    def perform_save(spell, owner):
        print(f"Performing save against {spell.type}...")

        # Collect inputs (to be passed from the GUI or external calls)
        save_inputs = SpellAttackHandler.get_save_inputs()

        # Perform the spell save
        damage = spell.perform_save(
            **save_inputs
        )

        return damage

