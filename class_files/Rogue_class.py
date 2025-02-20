from abc import ABC, abstractmethod
from .Sneak_attack import SneakAttack

class Rogue(ABC):
    def __init__(self, level, subclass, fighting_style, str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod, prof_bonus, spell_mod, spell_DC):
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
        self.spell_mod = spell_mod
        self.spell_DC = spell_DC
        self.sneak_attack = SneakAttack(self)

    def attack(self, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    def perform_sneak_attack(self, hit, roll, include_crits):
        return SneakAttack.sneak_damage(hit, self.level, roll, include_crits)

    def to_dict(self):
        """Serialize Rogue instance to JSON."""
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
            "spell_mod": self.spell_mod,
            "spell_DC": self.spell_DC,
            "sneak_attack": self.sneak_attack.to_dict(),  # Serialize SneakAttack
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize Rogue instance from JSON."""
        instance = cls(
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
            spell_mod=data["spell_mod"],
            spell_DC=data["spell_DC"],
        )
        # Deserialize SneakAttack
        if "sneak_attack" in data:
            instance.sneak_attack = SneakAttack.from_dict(
                data["sneak_attack"], lambda name: instance
            )
        return instance

