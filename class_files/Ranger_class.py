from abc import ABC
from .Hunters_mark import HuntersMark
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Gloomstalker_subclass import Gloomstalker  # Only import for type hints

class Ranger(ABC):
    def __init__(self, level, subclass, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod, prof_bonus, spell_mod, spell_dc):
        self.level = level
        self.subclass = subclass
        self.fighting_style = fighting_style
        self.str = str_mod
        self.dex = dex_mod
        self.con = con_mod
        self.int = int_mod
        self.wis = wis_mod
        self.cha = cha_mod
        self.prof_bonus = prof_bonus
        self.spell_mod = spell_mod
        self.spell_dc = spell_dc

    @property
    def has_multiattack(self):
        return self.level >= 5

    def attack(self, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    def perform_huntersmark(self, hit, roll, include_crits):
        return HuntersMark.hunters_mark_dmg(hit, self.level, roll, include_crits)

    def HuntersmarkAdv(self, level, hunters_mark):
        return level >= 13 and hunters_mark

    def has_gloomstalker(self):
        return self.subclass == "Gloomstalker"

    def perform_dreadful_strikes(self, hit, roll, include_crits):
        if self.has_gloomstalker():
            from .Gloomstalker_subclass import Gloomstalker  # Import inside method to avoid circular import
            gloomstalker_ability = Gloomstalker(self.level, self.fighting_style, self.str, self.dex, self.con,
                                                self.int, self.wis, self.cha, self.prof_bonus, self.spell_mod, self.spell_dc)
            return gloomstalker_ability.dreadful_strikes(hit, roll, include_crits)
        return 0  # No extra damage if not Gloomstalker

    def level_up(self):
        self.level += 1
        print(f"{self.__class__.__name__} has leveled up to level {self.level}!")

        if self.level >= 3 and self.has_gloomstalker():
            print(f"{self.__class__.__name__} (Gloomstalker) gains subclass features at Level {self.level}!")

        return self