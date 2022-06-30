import json
from tbcgear import *
from currency import *
from util import *
from tradegoods import *
from recipereg import *
from recipebridge import *


def get_auction(filename="C:/Program Files (x86)/World of Warcraft/_classic_/WTF/Account/308707580#1/SavedVariables/auction.json"):
    # upate using auction_to_json.lua
    obj = json.load(open(filename))
    auction = {}
    for name,item in obj['Westfall_Alliance'].items():
        auction[name.lower()] = item['mr']
    return auction


def update_essences(auction):
    """replaces lesser essence price with greater essence price/3 if cheaper"""
    for x in auction:
        greater_essence = x.replace('lesser', 'greater')
        if "lesser" in x and "essence" in x and x.replace('lesser', 'greater') in auction:
            auction[x] = min(auction[x], auction[greater_essence]//3)


def add_recipe_prices(auction, filename):
    file = open(filename)
    obj = json.load(file)
    for x,y in obj.items():
        auction[x] = y


def main():
    directory = "data/"
    auction = get_auction()

    ench = json.load(open(directory+"tbc_enchants.json"))
    tail = json.load(open(directory+"tbc_tailoring.json"))
    leath = json.load(open(directory+"tbc_leatherworking.json"))
    black = json.load(open(directory+"tbc_blacksmithing.json"))

    tbc_gear = TBCGear()
    tbc_gear.parse(directory+"tbc_armor.json", ItemClass.ARMOR)
    tbc_gear.parse(directory+"tbc_weapons.json", ItemClass.WEAPON)

    ID_to_Mat.parse(ench)  # gets dust IDs for disenchant only
    ID_to_Mat.parse(tail)

    Disenchant.registerAuction(auction)
    Disenchant.registerIDtoName(ID_to_Mat.id_to_mat)
    Disenchant.registerGear(tbc_gear)

    Util.register(Disenchant, tbc_gear)

    TradeGoods(directory+"tbc_trade_goods.json").update_auction(auction)

    enchanting = RecipeRegistry()
    enchanting.recipes = RecipeBridge.parse(ench)
    enchanting.update_matCosts(auction)
    enchanting.update_craftable_matCosts()

    tailoring = RecipeRegistry()
    tailoring.recipes = RecipeBridge.parse(tail)
    tailoring.update_matCosts(auction)
    tailoring.update_craftable_matCosts()

    leatherworking = RecipeRegistry()
    leatherworking.recipes = RecipeBridge.parse(leath)
    leatherworking.update_matCosts(auction)
    leatherworking.update_craftable_matCosts()

    blacksmithing = RecipeRegistry()
    blacksmithing.recipes = RecipeBridge.parse(black)
    blacksmithing.update_matCosts(auction)
    blacksmithing.update_craftable_matCosts()


if __name__ == "__main__":
    main()