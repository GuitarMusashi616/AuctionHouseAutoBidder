import json
from util import *
from item import *
from id_to_mat import *
from disenchant import *

class TBCGear:
    def __init__(self):
        self.items = {}

    def parse(self, filename, itemClass):
        raw_items = json.load(open(filename))
        for item in raw_items:
            parsed = self.parse_item(item, itemClass)
            self.items[parsed[0]] = Item(*parsed)

    def parse_item(self, item, itemClass):
        split_link = item[0].split('/')
        html_name = split_link[-1]
        ID = int(split_link[-2][5:])
        rarInt = int(item[1][1:2])
        rarity = Rarity(rarInt)
        ilvl = int(item[2])
        return [html_name, ID, 0, itemClass, rarity, ilvl]

    def from_name(self, name):
        html_name = Util.to_html_name(name)
        if html_name in self.items:
            return self.items[html_name]