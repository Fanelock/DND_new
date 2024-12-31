from DND_weapons.Weapon_main import WeaponAttack
import random as rd
import math

class HuntersMark(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Hunters Mark", None)

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    @staticmethod
    def hunters_mark_dmg(hit, level, roll):
        if not hit:
            return 0
        dice_type = 8 if level >= 8 else 6
        return rd.randint(1, dice_type)*2 if roll == 20 else rd.randint(1, dice_type)

    def __str__(self):
        return f"Hunters Mark deals {self.dmg} damage!"