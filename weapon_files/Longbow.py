from ..Weapon_main import WeaponAttack
from ..class_files import Rogue, Ranger, Gloomstalker, Cleric, Paladin, Druid
from .. import AttackHandler
import random as rd

class Longbow(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Longbow", "Ranged")
        self.number = 1
        self.dice_type = 8
        self.dmg = 0
        self.supports_sneak_attack = True
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark=False, bonus = 0, smite=False, strike=False, include_crits=False):
        if isinstance(self.owner, Ranger) and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        base_dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)

        if fighting_style and callable(self.fighting_style):
            damage = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)
        else:
            damage = base_dmg
        damage += self.apply_bonus_damage(hit, roll, hunters_mark, mastery, smite, strike, sneak_attack, advantage,
                                            include_crits=include_crits)

        self.dmg = damage

        return hit, roll, self.dmg

    def apply_bonus_damage(self, hit, roll, hunters_mark, mastery, smite, strike, sneak_attack, advantage, include_crits):
        bonus_damage = 0

        if hunters_mark and hit:
            bonus_damage += self.owner.perform_huntersmark(hit, roll, include_crits=include_crits)

        if smite and hit:
            bonus_damage += self.owner.perform_smite(hit, roll, include_crits=include_crits)

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            bonus_damage = self.owner.perform_sneak_attack(hit, roll, include_crits=include_crits)

        if strike and self.owner.level >= 7:
            if hasattr(self.owner, "divine_strike"):
                bonus_damage += self.owner.divine_strike(hit, roll, include_crits=include_crits)
            elif hasattr(self.owner, "primal_strike"):
                bonus_damage += self.owner.primal_strike(hit, roll, include_crits=include_crits)

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            p = rd.randint(1, 8)
            if p <= self.owner.wis:
                bonus_damage += self.owner.dreadful_strikes(hit, roll, include_crits=include_crits)
            bonus_damage += 0

        return bonus_damage

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                        include_crits=False, sneak_attack =False, hunters_mark=False, bonus = 0, smite =False, strike=False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        for _ in range(num_attacks):
            action_damage = 0
            for _ in range(attacks_per_action):  # Perform multiple attacks in one action
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
                    strike=strike,
                    include_crits=include_crits
                )

                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1

            results.append(action_damage)
            total_damage += action_damage

        overall_avg_damage = total_damage / (num_attacks * attacks_per_action)
        hit_avg_damage = total_hit_damage / hit_count

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Longbow deals {self.dmg} damage to the target!"