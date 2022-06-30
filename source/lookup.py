from urllib.request import urlopen
from bs4 import BeautifulSoup
from profitfinder import *
import socket


class LookupPrices:
    """Retreives Auction Data from NexusHub"""

    url = "https://nexushub.co/wow-classic/items/westfall-alliance/"
    title = "#app > div.app-view > div > header > div.container > div > div.item-profile-data-info > h1"
    body = "#app > div.app-view > div > div > div > main > section:nth-child(1) > div > div.row-margin > " \
           "div.module.col-b.stats.wow-classic_module_2l8-b > div.body "
    dic = {
        "Market Value": "div:nth-child(2) > div.col-2 > span.data-price",
        "Historical Value": "div:nth-child(3) > div.col-2 > span.data-price",
        "Minimum Buyout": "div:nth-child(4) > div.col-2 > span.data-price",
        "Quantity": "div:nth-child(5) > div.col-2 > span.data-price",
    }

    def __init__(self):
        self.dfbuilder = DFBuilder()

    @classmethod
    def lookup(cls, itemName):
        dfbuilder = DFBuilder()
        item_data = cls.get_item_data(itemName)
        cls.item_data_to_df(item_data, dfbuilder)
        return dfbuilder.to_df()

    @staticmethod
    def get_page(url):
        try:
            page = urlopen(url, timeout=3)
        except socket.timeout:
            return
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def to_html(name):
        return name.lower().replace(" ", "-").replace("'", "")

    @classmethod
    def matCost_links(cls, recipereg):
        return [cls.to_html(x) for x in recipereg.matCosts]

    @classmethod
    def get_item_data(cls, itemName):
        url = cls.url + cls.to_html(itemName)
        soup = cls.get_page(url)
        if soup:
            title = soup.select_one(cls.title)
            body = soup.select_one(cls.body)

            buffer = {"Name": title.get_text()}
            for col, sel in cls.dic.items():
                tag = body.select_one(sel)
                if tag:
                    val = tag.get_text().strip()
                    buffer[col] = val
                else:
                    raise IndexError(f"tag not found at {col}")
            return buffer

    @classmethod
    def item_data_to_df(cls, item_data, dfbuilder):
        for col, val in item_data.items():
            dfbuilder.add(col, val)

    def save(self, filename):
        df = self.dfbuilder.to_df()
        df.to_csv(filename, index=None)