from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack
from ..class_files import Rogue, Ranger, Gloomstalker, Cleric

class Dagger(WeaponAttack):
    def __init__(self, owner, bonus = 0):
        super().__init__(owner, "Dagger", "Light")
        self.number = 1
        self.dice_type = 4
        self.dmg = 0
        self.supports_sneak_attack = True
        self.bonus = bonus

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark=False, bonus = 0):
        if self.owner == Ranger and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        if self.owner == Rogue and advantage == True:
            sneak_attack = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus = self.bonus)

        base_dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus = self.bonus)

        if hasattr(self, 'fighting_style') and callable(self.fighting_style) and fighting_style != "TWF":
            damage = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus)
        else:
            damage = base_dmg

        print("post fighting style:", self.dmg)

        if hunters_mark and hit:
            damage += self.owner.perform_huntersmark(hit, roll)

        if isinstance(self.owner, Rogue) and (sneak_attack or advantage):
            sneak_attack_applied = False  # Flag to track if sneak attack has been applied
            #Apply sneak attack only once
            if advantage and hit and not sneak_attack_applied:
                sneak_dmg = self.owner.perform_sneak_attack(hit, advantage, roll)
                self.dmg += sneak_dmg
                sneak_attack_applied = True

        if isinstance(self.owner, Gloomstalker) and self.owner.level >= 3:
            dread = self.owner.dreadful_strikes(hit, roll)
            self.dmg += dread

        if isinstance(self.owner, Cleric) and self.owner.level >= 7:
            divine = self.owner.divine_strike(hit, roll)
            self.dmg += divine

        print("end dmg:", self.dmg)

        return hit, roll, base_dmg

    def simulate_attacks(self, ac, num_attacks=1000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, sneak_attack = False, hunters_mark=False, bonus=0):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        if self.owner.level >= 5:
            if mastery and self.owner.fighting_style != "TWF":
                attacks_per_action += 1  # Add a mastery attack (without modifiers for mastery) if not TWF
            if self.owner.fighting_style == "TWF":
                attacks_per_action += 1  # Add an additional TWF attack (with modifiers)

        elif self.owner.level < 5:
            attacks_per_action = 2  # One normal and one mastery attack
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
                        sneak_attack = sneak_attack,
                        hunters_mark=hunters_mark,
                        bonus=bonus
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
        overall_avg_damage = total_damage / (attacks_per_action * num_attacks)
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Dagger deals {self.dmg} damage to the target!"