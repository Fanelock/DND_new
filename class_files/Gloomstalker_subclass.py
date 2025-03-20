import random as rd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Ranger_class import Ranger

class Gloomstalker:
    def __init__(self, level, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                prof_bonus, spell_mod, spell_dc):
        from .Ranger_class import Ranger
        self.ranger_base = Ranger(level, "Gloomstalker", fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod,
                                cha_mod, prof_bonus, spell_mod, spell_dc)

    def dreadful_strikes(self, hit, roll, include_crits):
        dread_dmg = 0
        dice_type = 8 if self.ranger_base.level >= 11 else 6
        print(dice_type)
        if not hit:
            return 0
        elif roll == 20 and include_crits:
            return sum([rd.randint(1, dice_type) for _ in range(4)])
        return sum([rd.randint(1, dice_type) for _ in range(2)])