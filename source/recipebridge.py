from recipe import *

class RecipeBridge:
    def __init__(self, recipeObj):
        # format - ['Enchant Chest - Minor Health','15','70','90','110','https://tbc.wowhead.com/item=10940/strange-dust','Trainer']
        self.recipeObj = recipeObj

    @classmethod
    def parse(cls, recipeObjs):
        recipes = []
        for recipeObj in recipeObjs:
            recipes.append(cls(recipeObj).get_recipe())
        return recipes

    @staticmethod
    def shorten_mat_names(mats):
        return [x.split('/')[-1].replace('-', ' ').replace('rs ', "r's ") for x in mats]

    def get_mats(self):
        stack = []
        output = 1
        mats = self.recipeObj[5:-1]
        mats = self.shorten_mat_names(mats)

        for name_or_num in mats:
            try:
                amount = int(name_or_num)
                if not stack:
                    output = amount
                    continue

                name, _ = stack.pop()
                stack.append((name, amount))

            except ValueError:
                name = name_or_num
                stack.append((name, 1))

        return stack, output

    def get_skills(self):
        skills = self.fill_empty_skill_vals(self.recipeObj[1:5])
        return [int(x) for x in skills]

    def fill_empty_skill_vals(self, skills):
        for i in range(len(skills) - 1, -1, -1):
            if not skills[i]:
                try:
                    skills[i] = skills[i + 1]
                except IndexError:
                    skills[i] = 0
        return skills

    def get_recipe(self):
        name = self.recipeObj[0]

        skills = self.get_skills()
        mats, output = self.get_mats()

        source = self.recipeObj[-1]

        return Recipe(name, skills, mats, source, output)


