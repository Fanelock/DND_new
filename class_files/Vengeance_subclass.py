from .Hunters_mark import HuntersMark
import random as rd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Ranger_class import Paladin

class Vengeance:
    def __init__(self, level, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                prof_bonus, spell_mod, spell_dc):
        from .Paladin_class import Paladin
        self.paladin_base = Paladin(level, "Vengeance", fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod,
                        cha_mod, prof_bonus, spell_mod, spell_dc)

    def perform_huntersmark(self, hit, roll, include_crits):
        return HuntersMark.hunters_mark_dmg(hit, self.paladin_base.level, roll, include_crits)