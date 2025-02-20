from DND_weapons.Weapon_main import WeaponAttack
import random as rd
import math

class SneakAttack(WeaponAttack):
    def __init__(self, owner):
        super().__init__(owner, "Sneak Attack", None)
        self.dmg = 0

    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style):
        pass

    @staticmethod
    def sneak_damage(hit, level, roll, include_crits):
        dice_number = math.ceil(level / 2)
        dmg = 0  # Reset the damage for each sneak attack calculation
        if hit:  # Only calculate sneak attack if the attack hits
            if roll == 20 and include_crits == True:  # Critical hit doubles the dice
                for _ in range(2 * dice_number):
                    dmg_roll = rd.randint(1, 6)
                    dmg += dmg_roll
            else:  # Normal hit
                for _ in range(dice_number):
                    dmg_roll = rd.randint(1, 6)
                    dmg += dmg_roll
        return dmg

    def __str__(self):
        return f"Sneak Attack deals {self.dmg} damage!"

    def to_dict(self):
        """Convert the SneakAttack instance to a dictionary."""
        return {
            "owner": self.owner.name,  # Assuming `owner` has a `name` attribute for identification
            "dmg": self.dmg,
        }

    @classmethod
    def from_dict(cls, data, owner_lookup):
        """
        Recreate a SneakAttack instance from a dictionary.
        `owner_lookup` is a callable that retrieves the owner object by name.
        """
        owner = owner_lookup(data["owner"])  # Retrieve the owner object by its name
        instance = cls(owner)
        instance.dmg = data["dmg"]
        return instance