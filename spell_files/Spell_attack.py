from DND_weapons.Spell_main import Spell

class SpellAttack(Spell):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Attack")
        self.dmg = 0
        self.bonus = bonus

    def perform_attack(self, ac, dice_Number, dice_Type, advantage, disadvantage, sneak_attack = False, hunters_mark = False, bonus = 0, smite = False):
        hit, roll, advantage = super().spell_attack(ac, advantage, disadvantage, bonus = self.bonus)

        self.dmg = self.calc_dmg(hit, roll, dice_Number, dice_Type, bonus = self.bonus)

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit, roll)

        if smite and hit:
            self.dmg += self.owner.perform_smite(hit, roll)

        return hit, roll, self.dmg

    def simulate_attacks(self, ac=None, save_bonus=None, dice_number=0, dice_type=0, num_attacks=10000, advantage=False,
                            disadvantage=False, half_dmg=False, sneak_attack = False, hunters_mark=False, include_crits = False, bonus = 0, smite = False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        for _ in range(num_attacks):
            while True:
                if ac > 0:  # Spell Attack
                    hit, roll, damage = self.perform_attack(ac, dice_number, dice_type, advantage, disadvantage, sneak_attack=sneak_attack, hunters_mark=hunters_mark, bonus = self.bonus, smite = smite)
                elif save_bonus is not None:  # Spell Save
                    hit, roll, damage = self.perform_attack(save_bonus, dice_number, dice_type, advantage, disadvantage,
                                                            half_dmg, sneak_attack=sneak_attack, hunters_mark=hunters_mark, bonus = self.bonus)
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