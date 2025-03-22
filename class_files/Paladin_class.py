from abc import ABC, abstractmethod
from .Smite import Smite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Vengeance_subclass import Vengeance

class Paladin(ABC):
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

    def perform_smite(self, hit, roll, include_crits):
        return Smite.smite_dmg(hit, roll, include_crits)

    def has_vengeance(self):
        return self.subclass == "Vengeance"

    def level_up(self):
        self.level += 1
        print(f"{self.__class__.__name__} has leveled up to level {self.level}!")

        if self.level >= 3 and self.has_vengeance():
            print(f"{self.__class__.__name__} (Vengeance) gains subclass features at Level {self.level}!")

        return self