from DND_weapons.class_files import Rogue


class AttackHandler:
    @staticmethod
    def get_attack_inputs():

        inputs = {
            "ac": int(input("Enter the target's AC (Armor Class): ")),
            "dex": input("Is the attack using Dexterity? (1/0): ").strip().lower() == "1",
            "advantage": input("Does the attack have advantage? (1/0): ").strip().lower() == "1",
            "disadvantage": input("Does the attack have disadvantage? (1/0): ").strip().lower() == "1",
            "mastery": input("Does the attacker have mastery? (1/0): ").strip().lower() == "1",
        }
        return inputs

    @staticmethod
    def perform_attack(weapon, owner):
        print(f"Attacking with {weapon.name}...")

        # Collect user inputs
        attack_inputs = AttackHandler.get_attack_inputs()

        # Perform the attack
        damage = weapon.perform_attack(
            **attack_inputs, fighting_style = owner.fighting_style,
            sneak_attack=owner.sneak_attack_handler if isinstance(owner, Rogue) and getattr(weapon, 'supports_sneak_attack', False) else None
        )

        return damage
