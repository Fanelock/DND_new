from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack
from ..class_files import Rogue

class Dagger(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Dagger", "Light")
        self.number = 1
        self.dice_type = 4
        self.dmg = 0
        self.supports_sneak_attack = True

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack: SneakAttack = None):
        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex)

        self.dmg = self.apply_fighting_style(hit, roll, self.number, self.dice_type, dex)

        if fighting_style == None:
            if mastery:
                hit2, roll2, advantage2 = super().attack_roll(ac, dex, advantage, disadvantage)  # Second attack roll
                second_attack_dmg = self.calc_dmg(hit2, roll2, self.number, self.dice_type, dex)

                self.dmg += second_attack_dmg

                if second_attack_dmg != 0:
                    self.dmg += second_attack_dmg - self.owner.dex

        if isinstance(self.owner, Rogue):
            sneak_attack_applied = False  # Flag to track if sneak attack has been applied

            # Apply sneak attack only once, regardless of whether the first or second attack hits
            if (advantage and hit and not sneak_attack_applied):
                sneak_dmg = sneak_attack.sneak_damage()
                self.dmg += sneak_dmg
                sneak_attack_applied = True  # Set the flag to True so that we don't apply it again

            if (advantage and hit2 and not sneak_attack_applied):  # Only apply sneak attack if it's not already applied
                sneak_dmg = sneak_attack.sneak_damage()
                self.dmg += sneak_dmg
                sneak_attack_applied = True

        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=1000, dex=False, advantage=False, disadvantage=False, mastery=False, include_crits=False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        for _ in range(num_attacks):
            while True:
                # Perform the attack with the provided parameters
                hit, roll, damage = self.perform_attack(
                    ac=ac,
                    dex=dex,
                    advantage=advantage,
                    disadvantage=disadvantage,
                    mastery=mastery,
                    fighting_style=self.owner.fighting_style
                )

                # If critical hits are allowed, or this roll is not a crit, exit the loop
                if include_crits or roll != 20:
                    break

            # Collect damage results
            results.append(damage)
            total_damage += damage
            if hit:
                total_hit_damage += damage
                hit_count += 1

        # Calculate averages
        overall_avg_damage = total_damage / num_attacks
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Dagger deals {self.dmg} damage to the target!"