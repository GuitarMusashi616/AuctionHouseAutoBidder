class Currency:
    COIN_VALUES = {'g':10000, 's':100, 'c':1}

    def __init__(self, value):
        self.value = round(value)

    def __add__(self, other):
        return Currency(self.value + int(other))

    def __int__(self):
        return self.value

    def __lt__(self, other):
        return self.value < int(other)

    @classmethod
    def from_coins(cls, gold, silver, copper):
        return cls(gold * 100 * 100 + silver * 100 + copper)

    @classmethod
    def from_str(cls, string):
        coin_types = string.split(' ')
        value = 0
        for coin in coin_types:
            val = coin[:-1]
            metal = coin[-1]
            try:
                value += int(val) * cls.COIN_VALUES[metal]
            except ValueError as e:
                raise(ValueError(f"Value part of currency {coin} could not turned into an integer\n{e}"))
            except IndexError as e:
                raise(IndexError(f"metal {metal} from {coin} is not in Currency.COIN_VALUES"))
        return Currency(value)

    def __repr__(self):
        # try:
        value = round(self.value)
        # except OverflowError:
        #     value = self.value
        gold = value // 10000
        silver = value % 10000 // 100
        copper = value % 100

        ls = []
        if gold > 0:
            ls.append(str(gold) + 'g')

        if silver > 0:
            ls.append(str(silver) + 's')

        if copper > 0:
            ls.append(str(copper) + 'c')

        return ' '.join(ls)