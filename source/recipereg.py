import math
import json
import socket

from currency import Currency
from lookup import LookupPrices


class RecipeRegistry:
    def __init__(self):
        self.recipes = []
        self.matCosts = {}

    def update_matCosts(self, auction):
        # auction format - auction['linen cloth'] = 200
        if type(auction) is str:
            auction = json.load(open(auction))
        self.init_unique_matCosts()
        for i, v in self.matCosts.items():
            if i in auction:

                self.matCosts[i] = auction[i]

    @staticmethod
    def download(item_name, key='Historical Value'):
        try:
            item_data = LookupPrices.get_item_data(item_name)
            if item_data:
                val = Currency.from_str(item_data[key]).value
                print(item_name, item_data[key])
                return val
        except (socket.timeout, IndexError):
            return

    def download_matCosts(self, filename, key='Historical Value'):
        self.init_unique_matCosts()
        for i in self.matCosts.items():
            val = self.download(i, key)
            if val:
                self.matCosts[i] = val
        json.dump(self.matCosts, open(filename,"w"))

    def download_recipeCosts(self, filename, key='Historical Value'):
        recipe_prices = {}
        for recipe in self.recipes:
            val = self.download(recipe.name, key)
            if val:
                recipe_prices[recipe.name.lower()] = val
        json.dump(recipe_prices, open(filename, "w"))

    def update_craftable_matCosts(self, verbose=True):
        # eg. bolt of silk cloth or silk cloth x 4
        if verbose:
            print("Updating matCosts with craftable mat matCosts")

        self.recipes.sort(key=lambda x: x.req)
        for recipe in self.recipes:
            # todo: something about the 's in names
            self.update_matCost(recipe, verbose)

        if verbose:
            print()

    def update_matCost(self, recipe, verbose):
        dict_key = recipe.name.lower()
        self._update_matCost(recipe, verbose, dict_key)
        self._update_matCost(recipe, verbose, dict_key.replace("'s","s"))

    def _update_matCost(self, recipe, verbose, dict_key):
        if dict_key in self.matCosts:
            old_price = self.matCosts[dict_key]
            try:
                new_price = recipe.get_cost(self.matCosts)
            except IndexError:
                return

            if not old_price or new_price < old_price:
                self.matCosts[dict_key] = new_price
                if verbose:
                    print(f"{recipe.name} ({Currency(old_price)}) "
                          f"is now ({Currency(new_price)})")

    def find_recipe(self, name):
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe

    def show_matCosts(self, name):
        recipe = self.find_recipe(name)
        recipe.show_matCosts(self.matCosts)

    def __repr__(self):
        return repr(self.matCosts)

    def get(self, name):
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe

        raise KeyError(f"{name} could not be found");

    def get_craftable(self, skill):
        craftables = []
        for recipe in self.recipes:
            if recipe.is_craftable(skill):
                craftables.append(recipe)
        return craftables
        # return recipes with prob of skillup greater than 1 and craftable

    def init_unique_matCosts(self):
        for recipe in self.recipes:
            for mat in recipe.mats:
                if mat[0] not in self.matCosts:
                    self.matCosts[mat[0]] = False

    def get_recommended(self, skill, raise_error=False):
        craftables = self.get_craftable(skill)
        craftables.sort(key=lambda x: x.cost_per_skillup(skill, self.matCosts, raise_error))
        return [(x, Currency(x.cost_per_skillup(skill, self.matCosts, raise_error))) for x in craftables]

    def get_recommended_for_levels(self, start, end, raise_error=False):
        dic = {}
        for i in range(start, end):
            dic[i] = self.get_recommended(i, raise_error)[0]
        return dic

    # recommended for profit - (price of selling or disenchanting) - material cost (unless sellable on AH) (try just materials)
    def get_recommended_for_profit(self, skill):
        craftables = self.get_craftable(skill)
        craftables.sort(key=lambda x: x.get_cost(skill, self.matCosts))


