import json
import math
from item import *
from util import *
from currency import *


class TradeGoods:
    def __init__(self, filename="tbc_trade_goods.json"):
        self.raw_trade_goods = json.load(open(filename))
        self.items = self.process()

    def process_buy_price(self, money):
        if money[:9] == 'moneygold':
            return int(money[9:]) * 10000
        elif money[:11] == 'moneysilver':
            return int(money[11:]) * 100
        elif money[:11] == 'moneycopper':
            return int(money[11:])
        else:
            print(money)
            raise ValueError("dafuq das not monay")

    def process_trade_good(self, tg):
        quantity = self.process_quantity(tg)
        if not quantity:
            return
        name = tg[0]
        ID = int(tg[1])
        rarInt = int(tg[2])
        ilvl = int(tg[3])
        buyPrice = sum([self.process_buy_price(money) for money in tg[5:]])
        buyPrice = math.ceil(buyPrice / quantity)
        return Item(name, ID, buyPrice, ItemClass.TRADEGOODS, Rarity(rarInt), ilvl)

    def process(self):
        items = []
        for trade_good in self.raw_trade_goods:
            item = self.process_trade_good(trade_good)
            items.append(item)
        return items

    def process_quantity(self, tg):
        if tg[4] == None:
            return 1

        if tg[4][:7] != 'glow q1':
            return

        return int(tg[4][7:])

    def update_auction(self, auction, verbose=True):
        if verbose:
            print("Updating auction with trade goods")
        for item in self.items:
            try:
                name = item.name.lower()
                if name not in auction:
                    if verbose:
                        print(f"{item.name} initialized to ({Currency(item.sellPrice)})")
                    auction[name] = item.sellPrice
                elif auction[name] > item.sellPrice:
                    if verbose:
                        print(f"{item.name} ({Currency(auction[name])}) now costs ({Currency(item.sellPrice)})")
                    auction[name] = item.sellPrice
            except (AttributeError, KeyError):
                pass
        if verbose:
            print()

