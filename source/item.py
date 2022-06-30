class Item:
    def __init__(self, name, idx, sellPrice, classID, itemRarity, itemLevel):
        self.name = name
        self.id = idx
        self.sellPrice = sellPrice
        self.classID = classID
        self.itemRarity = itemRarity
        self.itemLevel = itemLevel
        self.buyoutPrice = None

    def __str__(self):
        string = (
            f"id:\t{self.id}\nname:\t{self.name}\nvalue:\t{self.sellPrice}\nclass:\t{self.classID}\nrarity:\t{self.itemRarity}\nilvl:\t{self.itemLevel}")
        return string

    def __repr__(self):
        return f"{self.name}"

    def setBuyout(self, value):
        self.buyoutPrice = value
