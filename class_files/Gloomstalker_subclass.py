from .Ranger_class import Ranger
import random as rd

class Gloomstalker(Ranger):
    def __init__(self, level, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                    prof_bonus, spell_mod, spell_DC):
        super().__init__(level, "Gloomstalker", fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod,
                    cha_mod, prof_bonus, spell_mod, spell_DC)

    def dreadful_strikes(self, hit, roll, include_crits):
        dread_dmg = 0
        dice_type = 8 if self.level >= 11 else 6
        if not hit:
            return 0
        elif roll == 20 and include_crits == True:
            return sum([rd.randint(1, dice_type) for _ in range(4)])
        return sum([rd.randint(1, dice_type) for _ in range(2)])
