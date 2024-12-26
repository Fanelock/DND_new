from DND_weapons.Spell_main import Spell

class SpellSave(Spell):
    def __init__(self, owner):
        super().__init__(owner, "Save")
        self.dmg = 0

    def perform_attack(self, save_bonus, dice_number, dice_type, advantage, disadvantage, half_dmg):
        hit, roll, advantage = super().spell_save(save_bonus, advantage, disadvantage)

        self.dmg = self.calc_dmg_save(hit, roll, half_dmg, dice_number, dice_type)


        return hit, roll, self.dmg

    def simulate_attacks(self, ac=None, save_bonus=None, dice_number=1, dice_type=6, num_attacks=1000, advantage=False,
                         disadvantage=False, half_dmg=False, include_crits = False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        for _ in range(num_attacks):
            while True:
                if ac > 0:  # Spell Attack
                    hit, roll, damage = self.perform_attack(ac, dice_number, dice_type, advantage, disadvantage, half_dmg)
                elif save_bonus is not None:  # Spell Save
                    hit, roll, damage = self.perform_attack(save_bonus, dice_number, dice_type, advantage, disadvantage,
                                                            half_dmg)
                else:
                    raise ValueError("Either 'ac' or 'save_bonus' must be provided.")
                if include_crits or roll != 20:
                    break

            results.append(damage)
            total_damage += damage
            if hit:
                total_hit_damage += damage
                hit_count += 1

        overall_avg_damage = total_damage / num_attacks
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Spell deals {self.dmg} damage to the target!"