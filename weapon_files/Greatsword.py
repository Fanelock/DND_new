import random as rd
from .. import AttackHandler
from ..Weapon_main import WeaponAttack
from ..class_files import Ranger, Gloomstalker

class Greatsword(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Greatsword", "Two-Handed")
        self.number = 2
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = False

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=None, hunters_mark = False):
        if isinstance(self.owner, Ranger) and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex)

        self.dmg = self.fighting_style(hit, roll, self.number, self.dice_type, dex)

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit)

        if mastery and not hit:
            self.dmg += self.owner.str

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            dread = self.owner.dreadful_strikes(hit)
            self.dmg += dread

        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=1000, dex=False, advantage=False, disadvantage=False, mastery=False, include_crits=False, hunters_mark=False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        for _ in range(num_attacks):
            action_damage = 0
            for _ in range(attacks_per_action):  # Perform multiple attacks in one action
                while True:
                    hit, roll, damage = self.perform_attack(
                        ac=ac,
                        dex=dex,
                        advantage=advantage,
                        disadvantage=disadvantage,
                        mastery=mastery,
                        fighting_style=self.owner.fighting_style,
                        hunters_mark=hunters_mark
                    )
                    if include_crits or roll != 20:
                        break
                if hit:
                    action_damage += damage
                    total_hit_damage += damage
                    hit_count += 1
                if not hit and mastery:
                    action_damage += damage

            # Collect damage results
            results.append(action_damage)
            total_damage += action_damage

        # Calculate averages
        overall_avg_damage = total_damage / (attacks_per_action * num_attacks)
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Greatsword deals {self.dmg} damage to the target!"