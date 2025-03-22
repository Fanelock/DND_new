import random as rd
from .. import AttackHandler
from ..Weapon_main import WeaponAttack
from ..class_files import Ranger, Gloomstalker, Cleric, Paladin, Druid

### This is the baseline for all Weapon-instances except for "dagger" and "shortsword"
### Additionally, weapons with sneak attack pass two more variables into the function "apply_bonus_damage", those being
### the variables "advantage" and "sneak_attack"

class Greatsword(WeaponAttack):
    ### Calls MotherClass "WeaponAttack" and sets base parameters for "Greatsword"
    def __init__(self, owner, bonus=0):
        super().__init__(owner, "Greatsword", "Two-Handed")
        self.number = 2
        self.dice_type = 6
        self.dmg = 0
        self.supports_sneak_attack = False
        self.hit_count = 0
        self.bonus = bonus

    ### Performs the Attack action with all relevant additional variables like fighting style, advantage etc.
    def perform_attack(self, ac, dex, advantage, disadvantage, mastery, fighting_style, sneak_attack=False, hunters_mark=False, bonus = 0, smite=False, strike = False, include_crits=False):
        if isinstance(self.owner, Ranger) and self.owner.HuntersmarkAdv(self.owner.level, hunters_mark):
            advantage = True

        ### Rolls primary attack roll
        hit, roll, advantage = super().attack_roll(ac, dex, advantage, disadvantage, bonus=self.bonus)

        ### Calculates primary damage based on primary attack roll
        base_dmg = self.calc_dmg(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)

        ### Checks if a fighting style is available and calls MotherClass function "fighting_style", adds it to variable damage.
        ### If no fighting style is available, sets damage to base_dmg from the first attack.
        if fighting_style and callable(self.fighting_style):
            damage = self.fighting_style(hit, roll, self.number, self.dice_type, dex, bonus=self.bonus, include_crits=include_crits)
        else:
            damage = base_dmg

        ### Calls function "apply_bonus_damage" for additional damage variables like hunters mark, smite, divine & primal strike
        damage += self.apply_bonus_damage(hit, roll, hunters_mark, mastery, smite, strike, include_crits=include_crits)

        ### sets self.dmg to damage
        self.dmg = damage

        return hit, roll, self.dmg

    ### In weapons where sneak attack could be used, advantage and sneak_attack variable are also passed into "apply_bonus_dmg"
    def apply_bonus_damage(self, hit, roll, hunters_mark, mastery, smite, strike, include_crits):
        bonus_damage = 0

        ### Adds hunters mark, if applicable
        if hunters_mark and hit:
            bonus_damage += self.owner.perform_huntersmark(hit, roll, include_crits=include_crits)

        ### Adds smite, if applicable
        if smite and hit:
            bonus_damage += self.owner.perform_smite(hit, roll, include_crits=include_crits)

        ### Adds mastery property, if applicable
        if mastery and not hit:
            bonus_damage += self.owner.str

        ### Adds divine or primal strike, if applicable
        if strike and self.owner.level >= 7:
            if hasattr(self.owner, "divine_strike"):
                bonus_damage += self.owner.divine_strike(hit, roll, include_crits=include_crits)
            elif hasattr(self.owner, "primal_strike"):
                bonus_damage += self.owner.primal_strike(hit, roll, include_crits=include_crits)

        ### Adds dreadful strike from Ranger - Gloomstalker subclass if applicable
        if isinstance(self.owner, Ranger) and self.owner.has_gloomstalker() and self.owner.level >= 3:
            p = rd.randint(1, 8) # p is calculated via 2 combats per day, with each combat being 4 rounds
            # since dreadful strike can only be used once per turn, up to as many times as wisdom modifier, it is checked against
            # wisdom modifier to see if it should be executed
            if p <= self.owner.wis:
                bonus_damage += self.owner.perform_dreadful_strikes(hit, roll, include_crits=include_crits)

        ### returns bonus damage to "perform_attack" function above
        return bonus_damage

    ### This function simulates the 10'000 attacks. Initially, all variables are set to false, but can be changed in the GUI
    ### interface. the "dex"-variable, for example, makes it so that dexterity is used for a weapon instead of strength,
    ### which is used in ranged weapons and weapons of the type "finesse"
    def simulate_attacks(self, ac, num_attacks=10000, dex=False, advantage=False, disadvantage=False, mastery=False,
                            include_crits=False, hunters_mark=False, sneak_attack=False, bonus=0, smite=False, strike = False):
        total_damage = 0
        total_hit_damage = 0
        hit_count = 0
        results = []

        ### This counter sets the variable "attacks_per_action" to 2 if a class has the property "multi attack". in the following for loop,
        ### it influences the behaviour of how many attacks are performed per attack action
        attacks_per_action = 2 if getattr(self.owner, 'has_multiattack', False) else 1

        for _ in range(num_attacks): # "num_attacks" -> how many attacks are performed
            action_damage = 0
            for _ in range(attacks_per_action):  # "attacks_per_action" -> performs multiple attacks in one action as specified above
                hit, roll, damage = self.perform_attack(
                    ac=ac,
                    dex=dex,
                    advantage=advantage,
                    disadvantage=disadvantage,
                    mastery=mastery,
                    fighting_style=self.owner.fighting_style,
                    sneak_attack=sneak_attack,
                    hunters_mark=hunters_mark,
                    bonus=bonus,
                    smite=smite,
                    strike=strike,
                    include_crits=include_crits
                )

                ### This block accumulates the total damage in the variable "action_damage", as well as in the variable "total_hit_damage"
                ### The variable "hit_count" is then used to, in the end, calculate the average damage per hit
                action_damage += damage
                if hit:
                    total_hit_damage += damage
                    hit_count += 1

            results.append(action_damage)
            total_damage += action_damage # The variable "total_damage" collects the action_damage from above

        overall_avg_damage = total_damage / num_attacks # Calculates the average damage PER TURN by dividing the variable "total_damage"
                                                        # by the variable "num_attacks" which is 10'000
        hit_avg_damage = total_hit_damage / hit_count # Calculates average damage per hit

        ### Returns results into the GUI-function "simulate_attacks", which then passes the results on into the GUI-function
        ### "display_results"
        return results, overall_avg_damage, hit_avg_damage, hit_count, total_hit_damage

    def __str__(self):
        return f"Your Greatsword deals {self.dmg} damage to the target!"
