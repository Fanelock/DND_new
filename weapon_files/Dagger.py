from ..Weapon_main import WeaponAttack
from ..class_files import SneakAttack
from ..class_files import Rogue, Ranger

class Dagger(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Dagger", "Light")
        self.number = 1
        self.dice_type = 4
        self.dmg = 0
        self.supports_sneak_attack = True

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=None, hunters_mark=False):
        if self.owner == Ranger and self.owner.has_hunters_mark_advantage(self.owner.level, hunters_mark):
            advantage = True

        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage)

        self.dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex)

        if hunters_mark and hit:
            self.dmg += self.owner.perform_huntersmark(hit)

        if fighting_style == "TWF":
            hit2, roll2, advantage2 = super().attack_roll(ac, dex, advantage, disadvantage)
            self.dmg = self.fighting_style(hit2, roll2, self.number, self.dice_type, dex)
            if hunters_mark and hit2:
                self.dmg += self.owner.perform_huntersmark(hit2)
        else:
            self.dmg = self.fighting_style(hit, roll, self.number, self.dice_type, dex)

        if mastery:
            # Check if no fighting style is present (i.e., `fighting_style == ""` or `None`)
            if fighting_style != "TWF":  # Apply Mastery attack if no fighting style
                hit3, roll3, advantage3 = super().attack_roll(ac, dex, advantage, disadvantage)
                second_attack_dmg = self.calc_dmg(hit3, roll3, self.number, self.dice_type, dex)
                if hunters_mark and hit3:
                    second_attack_dmg += self.owner.perform_huntersmark(hit3)

                # Add second attack damage without adding modifier to damage
                if second_attack_dmg != 0:
                    self.dmg += second_attack_dmg - (self.owner.dex if dex else self.owner.str)

        if isinstance(self.owner, Rogue):
            sneak_attack_applied = False  # Flag to track if sneak attack has been applied

            # Apply sneak attack only once, regardless of whether the first or second attack hits
            if (advantage and hit and not sneak_attack_applied):
                sneak_dmg = sneak_attack.sneak_damage()
                self.dmg += sneak_dmg
                sneak_attack_applied = True  # Set the flag to True so that we don't apply it again

            if (advantage and hit2 and not sneak_attack_applied):  # Only apply sneak attack if it's not already applied
                sneak_dmg = sneak_attack.sneak_damage()
                self.dmg += sneak_dmg
                sneak_attack_applied = True

        return hit, roll, self.dmg

    def simulate_attacks(self, ac, num_attacks=1000, dex=False, advantage=False, disadvantage=False, mastery=False, include_crits=False, hunters_mark=False):
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
                        hunters_mark=hunters_mark
                    )
                    if include_crits or roll != 20:
                        break

                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1
                if not hit and mastery:
                    action_damage += self.owner.str

            # Collect damage results
            results.append(action_damage)
            total_damage += action_damage

        # Calculate averages
        overall_avg_damage = total_damage / (attacks_per_action * num_attacks)
        hit_avg_damage = total_hit_damage / hit_count if hit_count > 0 else 0

        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"You Dagger deals {self.dmg} damage to the target!"