from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack, Ranger, Rogue, Cleric, Gloomstalker, Druid
from .. import AttackHandler
import random as rd

class Shortsword(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Shortsword", "Light")
        self.number = 1
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = True
        self.attack_counter = 1
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark = False, bonus = 0, smite =False, strike = False):
        if self.owner == Ranger and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        if self.owner == Rogue and advantage == True:
            sneak_attack = True

        if mastery:
            advantage = self.attack_counter % 2 == 0

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit, roll)

        if smite and hit:
            self.dmg += self.owner.perform_smite(hit, roll)

        if fighting_style == "TWF":
            hit2, roll2, advantage2 = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)
            self.dmg = self.fighting_style(hit2, roll2, self.number, self.dice_type, dex)
            if hunters_mark and hit2:
                self.dmg += self.owner.perform_huntersmark(hit2, roll2)
        else:
            self.dmg = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            sneak_dmg = self.owner.perform_sneak_attack(hit, roll)
            self.dmg += sneak_dmg

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            p = rd.randint(1, 8)
            if self.owner.wis <= p:
                self.dmg += self.owner.dreadful_strikes(hit, roll)
            self.dmg += 0

        if strike and self.owner.level >= 7:
            if hasattr(self.owner, "divine_strike"):
                self.dmg += self.owner.divine_strike(hit, roll)
            elif hasattr(self.owner, "primal_strike"):
                self.dmg += self.owner.primal_strike(hit, roll)

        self.attack_counter += 1

        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, sneak_attack=False, hunters_mark=False, bonus=0, smite=False, strike=False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1
        if self.owner.fighting_style == "TWF":
            attacks_per_action += 1

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
                        strike=strike
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
        hit_avg_damage = total_damage / num_attacks

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Shortsword deals {self.dmg} damage to the target!"