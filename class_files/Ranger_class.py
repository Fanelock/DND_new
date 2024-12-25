from abc import ABC, abstractmethod

class Ranger(ABC):
    def __init__(self, level, subclass, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod, prof_bonus):
        self.level = level
        self.subclass = subclass
        self.fighting_style = fighting_style
        self.str = str_mod
        self.dex = dex_mod
        self.con = con_mod
        self.int = int_mod
        self.wis = wis_mod
        self.cha = cha_mod
        self.prof = prof_bonus

    def attack(self, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    def to_dict(self):
        return {
            "class_name": self.__class__.__name__,  # Identifies the class type
            "level": self.level,
            "subclass": self.subclass,
            "fighting_style": self.fighting_style,
            "str_mod": self.str,
            "dex_mod": self.dex,
            "con_mod": self.con,
            "int_mod": self.int,
            "wis_mod": self.wis,
            "cha_mod": self.cha,
            "prof_bonus": self.prof,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            level=data["level"],
            subclass=data.get("subclass"),
            fighting_style=data.get("fighting_style"),
            str_mod=data["str_mod"],
            dex_mod=data["dex_mod"],
            con_mod=data["con_mod"],
            int_mod=data["int_mod"],
            wis_mod=data["wis_mod"],
            cha_mod=data["cha_mod"],
            prof_bonus=data["prof_bonus"],
        )