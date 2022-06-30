from enum import Enum

class ItemClass(Enum):
    CONSUMABLE = 0
    CONTAINER  = 1
    WEAPON     = 2
    GEM        = 3
    ARMOR      = 4
    PROJECTILE = 6
    TRADEGOODS = 7
    RECIPE     = 9
    QUIVER     = 11
    QUEST      = 12
    KEY        = 13
    MISC       = 15


class Rarity(Enum):
    POOR      = 0
    COMMON    = 1
    UNCOMMON  = 2
    RARE      = 3
    EPIC      = 4
    LEGENDARY = 5

class Util:
    DONT_CAPITALIZE = {'a', 'an', 'the', 'for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'at', 'around', 'by', 'after',
                       'along', 'from', 'of', 'on', 'to', 'with', 'without'}

    @classmethod
    def register(cls, disenchant, gear):
        cls.disenchant = disenchant
        cls.gear = gear

    @classmethod
    def stylized_name(cls, html_name):
        name = html_name.replace("-", " ")  # .replace("s ", "'s ")
        words = [word[0].upper() + word[1:] for word in name.split(" ") if word not in cls.DONT_CAPITALIZE]
        return " ".join(words)

    @staticmethod
    def to_html_name(name):
        return name.lower().replace(" ", "-").replace("'", "")

    @classmethod
    def recipe_details(cls, name, recipereg):
        recipereg.show_matCosts(name)
        print()
        item = cls.gear.from_name(name)
        try:
            cls.disenchant.showChancesFor(item)
        except AttributeError:
            pass
