from .Ranger_class import Ranger
import random

class Gloomstalker(Ranger):
    def __init__(self, level, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                    prof_bonus, spell_mod, spell_DC):
        super().__init__(level, "Gloomstalker", fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod,
                    cha_mod, prof_bonus, spell_mod, spell_DC)

    def dreadful_strikes(self, hit):
        dread_dmg = 0
        dice_type = 8 if self.level >= 11 else 6
        if hit:
                dmg = random.randint(1, dice_type)
                dread_dmg += dmg
        return dread_dmg
