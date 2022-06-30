from util import *
from currency import *

class Recipe:
    def __init__(self, name, skills, mats, source, output=1):
        # format - Recipe('Bolt of Linen Cloth', [1, 25, 37, 50], [(2,'linen cloth')], '', 1)
        self.name = name
        self.mats = mats
        self.source = source
        self.output = output

        self.req = int(skills[0])
        self.yellow = int(skills[1])
        self.green = int(skills[2])
        self.grey = int(skills[3])

    def __repr__(self):
        return self.name

    def cost_per_skillup(self, skill, matCosts, raise_error=True):
        return self.get_cost(matCosts, raise_error) / self.get_chance(skill)

    def get_color(self, skill):
        if skill < self.req:
            return "unavailable"
        elif self.req <= skill < self.yellow:
            return "orange"
        elif self.yellow <= skill < self.green:
            return "yellow"
        elif self.green <= skill < self.grey:
            return "green"
        else:
            return "grey"

    def get_chance(self, skill):
        # skill up chance
        return min(1, (self.grey - skill) / (self.grey - self.yellow))

    def is_craftable(self, skill):
        return self.get_color(skill) != "grey" and self.get_color(skill) != "unavailable"

    def get_cost(self, matCosts, raise_error=True):
        total = 0
        for mat in self.mats:
            name = mat[0]
            amount = mat[1]
            if name in matCosts and matCosts[name] != False:
                total += amount * matCosts[name]
            else:
                if raise_error:
                    raise IndexError(f"missing {name} in matCosts")
                else:
                    return 8000000
        return total

    def show_matCosts(self, matCosts):
        for mat in self.mats:
            name = mat[0]
            amount = mat[1]
            print(f"{Util.stylized_name(name)} ({amount}) {Currency(matCosts[name])}")

    def mats_in_matCosts(self, matCosts):
        for mat in self.mats:
            if mat not in matCosts:
                return False
        return True