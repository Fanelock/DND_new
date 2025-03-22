from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack, Ranger, Rogue, Cleric, Gloomstalker, Druid
from .. import AttackHandler
import random as rd

### By the grace of God, the Omnissiah or whatever other Deity you believe in, do NOT touch this file
### it is being held together by hopes, dreams, and the equivalent of duct tape
### This is one of the two weapon-files which isn't standardized bc of its mastery property (the other being the dagger)
### So please, in the name of everything that is holy to you, don't touch this file and don't try to optimize it

class Shortsword(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Shortsword", "Light")
        self.number = 1
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = True
        self.attack_counter = 1
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark = False, bonus = 0, smite =False, strike = False, include_crits=False, use_twf = False):
        if self.owner == Ranger and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        if mastery:
            advantage = self.attack_counter % 2 == 0

        if self.owner == Rogue and advantage == True:
            sneak_attack = True

        self.dmg = 0

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)
        hit2, roll2, advantage2 = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        attack_1_dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)
        attack_2_dmg = 0
        fighting_style_dmg = 0
        dread_dmg = 0
        primal_dmg = 0
        divine_dmg = 0
        sneak_dmg = 0

        if hunters_mark and hit:
            attack_1_dmg += self.owner.perform_huntersmark(hit, roll)

        if smite and hit:
            attack_1_dmg += self.owner.perform_smite(hit, roll)

        if fighting_style == "TWF" and use_twf:
            self.dmg = 0
            attack_2_dmg = self.fighting_style(hit2, roll2, self.number, self.dice_type, dex, include_crits=include_crits)
            if hunters_mark and hit2:
                attack_2_dmg += self.owner.perform_huntersmark(hit2, roll2)
        elif fighting_style != "TWF" and fighting_style:
            fighting_style_dmg += self.fighting_style(hit2, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)


        attack_1_dmg += fighting_style_dmg
        attack_1_dmg += attack_2_dmg

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            sneak_dmg += self.owner.perform_sneak_attack(hit, roll, include_crits=include_crits)
            attack_1_dmg += sneak_dmg

        if isinstance(self.owner, Ranger) and self.owner.has_gloomstalker() and self.owner.level >= 3:
            p = rd.randint(1, 8)
            if p <= self.owner.wis:
                dread_dmg += self.owner.perform_dreadful_strikes(hit, roll, include_crits=include_crits)
            dread_dmg += 0

        if strike and self.owner.level >= 7:
            if hasattr(self.owner, "divine_strike"):
                divine_dmg += self.owner.divine_strike(hit, roll, include_crits=include_crits)
            elif hasattr(self.owner, "primal_strike"):
                primal_dmg += self.owner.primal_strike(hit, roll, include_crits=include_crits)

        attack_1_dmg +=  (dread_dmg + primal_dmg + divine_dmg)
        self.dmg = attack_1_dmg
        self.attack_counter += 1

        return hit, hit2, attack_2_dmg, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, sneak_attack=False, hunters_mark=False, bonus=0, smite=False, strike=False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        for _ in range(num_attacks):
            action_damage = 0
            use_twf = self.owner.fighting_style == "TWF"
            for _ in range(attacks_per_action):  # Perform multiple attacks in one action
                hit, hit2, attack_2_dmg, roll, damage = self.perform_attack(
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
                    include_crits=include_crits,
                    use_twf=use_twf
                )
                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1
                if hit2 and use_twf:
                    hit_count += 1
                    if not hit:
                        total_hit_damage += attack_2_dmg

                use_twf = False

            results.append(action_damage)
            total_damage += action_damage

        overall_avg_damage = total_damage / num_attacks
        hit_avg_damage = total_hit_damage / hit_count

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Shortsword deals {self.dmg} damage to the target!"