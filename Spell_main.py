import random as rd
from abc import ABC, abstractmethod

class Spell(ABC):
    def __init__(self, owner, type):
        self.owner = owner
        self.hit_roll = 0
        self.save_roll = 0
        self.type = type
        self.dmg = 0

    def spell_attack(self, ac, advantage, disadvantage):
        if advantage:
            hit_roll_1 = rd.randint(1,20)
            hit_roll_2 = rd.randint(1,20)
            self.hit_roll = max(hit_roll_1, hit_roll_2)
        elif disadvantage:
            hit_roll_1 = rd.randint(1, 20)
            hit_roll_2 = rd.randint(1, 20)
            self.hit_roll = min(hit_roll_1, hit_roll_2)
        else:
            self.hit_roll = rd.randint(1, 20)
        total = self.hit_roll + self.owner.spell_mod + self.owner.prof

        return total >= ac, self.hit_roll, advantage

    def spell_save(self, save_bonus, advantage, disadvantage):
        if advantage:
            save_roll_1 = rd.randint(1,20)
            save_roll_2 = rd.randint(1,20)
            self.save_roll = max(save_roll_1, save_roll_2)
        elif disadvantage:
            save_roll_1 = rd.randint(1, 20)
            save_roll_2 = rd.randint(1, 20)
            self.save_roll = min(save_roll_1, save_roll_2)
        else:
            self.save_roll = rd.randint(1, 20)
        total = self.save_roll + save_bonus

        return total >= self.owner.spell_DC, self.save_roll, advantage

    def calc_dmg(self, hit, roll, number, dice_type):
        self.dmg = 0
        if roll == 20:
            for i in range(2 * number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.spell_mod
            return self.dmg
        elif not hit:
            return self.dmg
        else:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.spell_mod
        return self.dmg

    def calc_dmg_save(self, hit, roll, half_dmg, number, dice_type):
        self.dmg = 0
        if roll == 20:
            for i in range(2 * number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.spell_mod
            return self.dmg
        elif not hit and half_dmg:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.spell_mod
            self.dmg //= 2
            return self.dmg
        elif not hit:
            return self.dmg
        else:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.spell_mod

        return self.dmg