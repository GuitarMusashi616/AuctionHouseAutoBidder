import pandas as pd

class DFBuilder:
    def __init__(self):
        self.dict = {}

    def add(self, col, val):
        if col not in self.dict:
            self.dict[col] = []
        self.dict[col].append(val)

    def to_df(self):
        return pd.DataFrame(self.dict)