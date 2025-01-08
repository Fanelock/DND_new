import random as rd
from .. import AttackHandler
from ..Weapon_main import WeaponAttack
from ..class_files import Ranger, Gloomstalker, Cleric, Paladin


class Greatsword(WeaponAttack):
    def __init__(self, owner, bonus=0):
        super().__init__(owner, "Greatsword", "Two-Handed")
        self.number = 2
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = False
        self.hit_count = 0
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark=False, bonus = 0, smite=False):
        if isinstance(self.owner, Ranger) and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)


        base_dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)
        print("normal damage:", base_dmg)
        if fighting_style and callable(self.fighting_style):
            damage = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)
        else:
            damage = base_dmg
        print("post fighint style:", damage)
        damage += self.apply_bonus_damage(hit, roll, hunters_mark, mastery, smite)

        print("post bonus:", damage)

        self.dmg = damage

        return hit, roll, self.dmg

    def apply_bonus_damage(self, hit, roll, hunters_mark, mastery, smite):
        bonus_damage = 0

        if hunters_mark and hit:
            bonus_damage += self.owner.perform_huntersmark(hit, roll)

        if smite and hit:
            bonus_damage += self.owner.perform_smite(hit, roll)

        if mastery and not hit:
            bonus_damage += self.owner.str

        #if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
        #    bonus_damage += self.owner.dreadful_strikes(hit, roll)

        if isinstance(self.owner, Cleric) and self.owner.level >= 7:
            bonus_damage += self.owner.divine_strike(hit, roll)

        return bonus_damage

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, hunters_mark=False, sneak_attack=False, bonus=0, smite=False):
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
                        sneak_attack=sneak_attack,
                        hunters_mark=hunters_mark,
                        bonus=bonus,
                        smite=smite,
                    )
                    if not include_crits and roll == 20:
                        roll = 19
                    if include_crits or roll != 20:
                        break

                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1

            results.append(action_damage)
            total_damage += action_damage

        overall_avg_damage = total_damage / (num_attacks * attacks_per_action)
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"Your Greatsword deals {self.dmg} damage to the target!"
