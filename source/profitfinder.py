from disenchant import *
from currency import *
from dfbuilder import *
import math


class ProfitFinder:
    def __init__(self, recipereg, armors):
        self.recipereg = recipereg
        self.armors = armors

    def best_deals_for_selling_directly(self, auction, sort="%"):
        """simply buying all the mats for each recipe then reselling it on the AH"""
        dfbuilder = DFBuilder()
        recipes = self.recipereg.recipes
        for recipe in recipes:
            if recipe.name.lower() in auction:
                try:
                    cost = recipe.get_cost(self.recipereg.matCosts)
                    revenue = auction[recipe.name.lower()]
                    dfbuilder.add("Recipe", f"{recipe.name} ({recipe.req})")
                    dfbuilder.add("Cost", Currency(cost))
                    dfbuilder.add("Revenue", Currency(revenue))
                    dfbuilder.add("Profit", Currency(revenue-cost))
                    dfbuilder.add("%", round((revenue-cost)*100/revenue,1))
                except IndexError:
                    pass  # skip if cost can't be calculated due to missing reagents

        return dfbuilder.to_df().sort_values(by=sort, ascending=False)

    def best_deals(self, sort="%", lvl=None, verbose=False):
        recipes = self.recipereg.get_craftable(lvl) if lvl else self.recipereg.recipes
        dfbuilder = DFBuilder()

        for recipe in recipes:
            item = self.armors.from_name(recipe.name)
            if item:
                try:
                    matCost = recipe.get_cost(self.recipereg.matCosts)
                    dePrice = Disenchant.calcItemPrice(item)
                    profit = dePrice - matCost
                    profitMargin = round((profit / dePrice) * 100, 1)

                    dfbuilder.add("Recipe", f"{recipe.name} ({recipe.req})")
                    dfbuilder.add("Cost", Currency(matCost))
                    dfbuilder.add("Revenue", Currency(dePrice))
                    dfbuilder.add("Profit", Currency(profit))
                    dfbuilder.add("%", profitMargin)

                except IndexError as e:
                    if verbose:
                        print(f"{recipe.name} ({recipe.req})",e)
                except ValueError:
                    pass  # if can't be disenchanted then skip

        return dfbuilder.to_df().sort_values(by=sort, ascending=False)