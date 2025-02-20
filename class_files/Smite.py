from DND_weapons.Weapon_main import WeaponAttack
import random as rd
import math

class Smite(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Smite", None)

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    @staticmethod
    def smite_dmg(hit, roll, include_crits):
        dice_type = 8
        if not hit:
            return 0
        elif roll == 20 and include_crits == True:
            return sum([rd.randint(1, dice_type) for _ in range(4)])
        return sum([rd.randint(1, dice_type) for _ in range(2)])

    def __str__(self):
        return f"Smite deals {self.dmg} damage!"

