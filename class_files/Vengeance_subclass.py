from .Paladin_class import Paladin
from .Hunters_mark import HuntersMark
import random as rd

class Vengeance(Paladin):
    def __init__(self, level, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod,
                    prof_bonus, spell_mod, spell_DC):
        super().__init__(level, "Vengeance", fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod,
                    cha_mod, prof_bonus, spell_mod, spell_DC)

    def perform_huntersmark(self, hit, roll):
        return HuntersMark.hunters_mark_dmg(hit, self.level, roll)