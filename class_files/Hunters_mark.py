from DND_weapons.Weapon_main import WeaponAttack
import random as rd
import math

class HuntersMark(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Hunters Mark", None)

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    @staticmethod
    def hunters_mark_dmg(hit, level, roll, include_crits):
        dice_type = 8 if level >= 8 else 6
        if not hit:
            return 0
        elif roll == 20 and include_crits == True:
            return sum([rd.randint(1, dice_type) for _ in range(2)])
        return rd.randint(1, dice_type)

    def __str__(self):
        return f"Hunters Mark deals {self.dmg} damage!"