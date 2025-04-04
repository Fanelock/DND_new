import random as rd
from abc import ABC, abstractmethod

class WeaponAttack(ABC):
    def __init__(self, owner, name, weapon_type):
        self.owner = owner
        self.hit_roll = 0
        self.name = name
        self.dmg = 0
        self.weapon_type = weapon_type

    def attack_roll(self, ac, dex, advantage, disadvantage, bonus=0):
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
        if dex:
            total = (self.hit_roll + self.owner.dex + self.owner.prof_bonus + bonus)
        else:
            total = (self.hit_roll + self.owner.str + self.owner.prof_bonus + bonus)

        return total >= ac, self.hit_roll, advantage

    def calc_dmg(self, hit, roll, number, dice_type, dex, bonus=0, include_crits = False):
        self.dmg = 0
        if roll == 20 and include_crits == True:
            for i in range(2 * number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.dex if dex else self.owner.str
            self.dmg += bonus
            return self.dmg
        elif not hit:
            return self.dmg
        else:
            for i in range(number):
                dmg_roll = rd.randint(1, dice_type)
                self.dmg += dmg_roll
            self.dmg += self.owner.dex if dex else self.owner.str
            self.dmg += bonus
        return self.dmg

    def fighting_style(self, hit, roll, number, dice_type, dex, bonus=0, include_crits = False):
        style = self.owner.fighting_style
        adjusted_dmg = 0
        if self.owner.level >= 2 and style != None:
            if style == "GWF" and self.weapon_type in {"Two-Handed", "Versatile"} and hit:
                self.dmg = 0
                if roll == 20 and include_crits == True:
                    for _ in range(2 * number):
                        dmg_roll = max(rd.randint(1, dice_type), 3)
                        adjusted_dmg += dmg_roll
                    adjusted_dmg += self.owner.str
                    adjusted_dmg += bonus
                    self.dmg = adjusted_dmg
                else:
                    for _ in range(number):
                        dmg_roll = max(rd.randint(1, dice_type), 3)
                        adjusted_dmg += dmg_roll
                    adjusted_dmg += self.owner.str
                    adjusted_dmg += bonus
                    self.dmg = adjusted_dmg
            if style == "Archery" and self.weapon_type == "Ranged" and hit:
                self.dmg += 2
            if style == "Dueling" and self.weapon_type in {"Versatile", "Light", "Finesse", "Meele"} and hit:
                self.dmg += 2
            if style == "TWF" and self.weapon_type == "Light" and hit:
                self.dmg = 0
                dmg_roll = 0
                if roll == 20 and include_crits:
                    for _ in range(2 * number):
                        adjusted_dmg = rd.randint(1, dice_type)
                        dmg_roll += adjusted_dmg
                else:
                    for _ in range(number):
                        dmg_roll = rd.randint(1, dice_type)
                dmg_roll += self.owner.dex if dex else self.owner.str
                dmg_roll += bonus
                self.dmg = dmg_roll
        return self.dmg

    @abstractmethod
    def __str__(self):
        pass

