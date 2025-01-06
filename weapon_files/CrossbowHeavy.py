import random as rd
from .. import AttackHandler
from ..Weapon_main import WeaponAttack
from ..class_files import Ranger, Gloomstalker, Rogue, Cleric, Paladin


class CrossbowHeavy(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Heavy Crossbow", "Ranged")
        self.number = 1
        self.dice_type = 10
        self.dmg = 0
        self.supports_sneak_attack = True
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False,
                    hunters_mark=False, bonus=0, smite =False):
        if self.owner == Ranger and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        if self.owner == Rogue and advantage == True:
            sneak_attack = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)

        self.dmg = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus = self.bonus)

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit, roll)

        if smite and hit:
            self.dmg += self.owner.perform_smite(hit, roll)

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            sneak_dmg = self.owner.perform_sneak_attack(hit, roll)
            self.dmg += sneak_dmg

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            dread = self.owner.dreadful_strikes(hit, roll)
            self.dmg += dread

        if isinstance(self.owner, Cleric) and self.owner.level >= 7:
            divine = self.owner.divine_strike(hit, roll)
            self.dmg += divine


        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, sneak_attack = False, hunters_mark=False, bonus=0, smite =False):
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
                    if include_crits or roll != 20:
                        break

                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1

            # Collect damage results
            results.append(action_damage)
            total_damage += action_damage

        # Calculate averages
        overall_avg_damage = total_damage / num_attacks
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Heavy Crossbow deals {self.dmg} damage to the target!"