import random as rd
from abc import ABC, abstractmethod

class Spell(ABC):
    def __init__(self, owner, type):
        self.owner = owner
        self.hit_roll = 0
        self.save_roll = 0
        self.type = type
        self.dmg = 0

    def get_owner_attribute(self, attr_name):
        if isinstance(self.owner, list):
            class_instance = next((cls for cls in self.owner if hasattr(cls, attr_name)), None)
            return getattr(class_instance, attr_name, 0) if class_instance else 0
        else:
            return getattr(self.owner, attr_name, 0)

    def spell_attack(self, ac, advantage, disadvantage, bonus = 0):
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
        total = (self.hit_roll + self.get_owner_attribute('spell_mod') + self.get_owner_attribute('prof') + bonus)

        return total >= ac, self.hit_roll, advantage

    def spell_save(self, save_bonus, advantage, disadvantage, bonus = 0):
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

        return total >= (self.get_owner_attribute('spell_dc') + bonus), self.save_roll, advantage

    def calc_dmg(self, hit, roll, number, dice_type, bonus = 0, include_crits=False):
        self.dmg = 0
        if roll == 20 and include_crits == True:
            for i in range(2 * number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += bonus
            return self.dmg
        elif not hit:
            return self.dmg
        else:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += bonus
        return self.dmg

    def calc_dmg_save(self, hit, roll, half_dmg, number, dice_type, bonus = 0, include_crits=False):
        self.dmg = 0
        if roll == 1 and include_crits == True:
            for i in range(2 * number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += bonus
            return self.dmg
        elif not hit and half_dmg:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += bonus
            self.dmg //= 2
            return self.dmg
        elif not hit:
            return self.dmg
        else:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += bonus

        return self.dmg