from abc import ABC, abstractmethod
from .Sneak_attack import SneakAttack

class Rogue(ABC):
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
        self.sneak_attack = SneakAttack(self)

    def attack(self, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    def perform_sneak_attack(self, hit, roll, include_crits):
        return SneakAttack.sneak_damage(hit, self.level, roll, include_crits)

    def level_up(self):
        self.level += 1
        print(f"{self.__class__.__name__} has leveled up to level {self.level}!")

        return self

