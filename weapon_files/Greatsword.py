import random as rd
from .. import AttackHandler
from ..Weapon_main import WeaponAttack

class Greatsword(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Greatsword", "Two-Handed")
        self.number = 2
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = False

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=None):
        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex)

        self.dmg = self.apply_fighting_style(hit, roll, self.number, self.dice_type, dex)

        if self.dmg == 0 and mastery == True:
            self.dmg = self.owner.str

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
        return f"You Greatsword deals {self.dmg} damage to the target!"

