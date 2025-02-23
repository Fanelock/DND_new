from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack
from ..class_files import Rogue, Ranger, Gloomstalker, Cleric, Paladin, Druid
import random as rd

class Dagger(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Dagger", "Light")
        self.number = 1
        self.dice_type = 4
        self.dmg = 0
        self.supports_sneak_attack = True
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark=False, bonus = 0, smite = False, strike = False, include_crits=False):
        if self.owner == Ranger and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        if self.owner == Rogue and advantage == True:
            sneak_attack = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus = self.bonus)
        hit2, roll2, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus = self.bonus, include_crits = include_crits)

        if hasattr(self, 'fighting_style') and callable(self.fighting_style) and fighting_style != "TWF":
            self.dmg = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits = include_crits)

        mastery_dmg = 0
        if mastery:
            mastery_dmg = self.calc_dmg(hit2, roll2, self.number, self.dice_type, dex, bonus=self.bonus, include_crits = include_crits)
            mastery_dmg -= (self.owner.dex if dex else self.owner.str)

        twf_dmg = 0
        if hasattr(self, 'fighting_style') and callable(self.fighting_style) and fighting_style == "TWF":
            if mastery:
                mastery_dmg += (self.owner.dex if dex else self.owner.str)
            if not mastery:
                twf_dmg = self.calc_dmg(hit2, roll2, self.number, self.dice_type, dex, bonus=self.bonus, include_crits = include_crits)

        self.dmg += mastery_dmg
        self.dmg += twf_dmg

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit, roll, include_crits=include_crits)

        if smite and hit:
            self.dmg += self.owner.perform_smite(hit, roll, include_crits=include_crits)

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            sneak_attack_applied = False  # Flag to track if sneak attack has been applied
            #Apply sneak attack only once
            if not sneak_attack_applied:
                sneak_dmg = self.owner.perform_sneak_attack(hit, roll, include_crits=include_crits)
                self.dmg += sneak_dmg
                sneak_attack_applied = True

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            p = rd.randint(1, 8)
            if p <= self.owner.wis:
                self.dmg += self.owner.dreadful_strikes(hit, roll, include_crits=include_crits)
            self.dmg += 0

        if strike and self.owner.level >= 7:
            if hasattr(self.owner, "divine_strike"):
                self.dmg += self.owner.divine_strike(hit, roll, include_crits=include_crits)
            elif hasattr(self.owner, "primal_strike"):
                self.dmg += self.owner.primal_strike(hit, roll, include_crits=include_crits)

        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, sneak_attack = False, hunters_mark=False, bonus=0, smite=False, strike = False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        if mastery or self.owner.fighting_style == "TWF":
            attacks_per_action += 1

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

            # Collect damage results
            results.append(action_damage)
            total_damage += action_damage

        # Calculate averages
        overall_avg_damage = total_damage / (num_attacks * attacks_per_action)
        hit_avg_damage = total_damage / num_attacks

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Dagger deals {self.dmg} damage to the target!"