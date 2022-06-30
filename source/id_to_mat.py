class ID_to_Mat:
    id_to_mat = {}

    @classmethod
    def parse(cls, jsonRecipes):
        linkGen = (cls.find_links(recipe) for recipe in jsonRecipes)
        for links in linkGen:
            for link in links:
                idx, mat = cls.get_id_mat(link)
                cls.put(idx, mat)

    @classmethod
    def put(cls, idx, name):
        if idx not in cls.id_to_mat:
            cls.id_to_mat[idx] = name

    @classmethod
    def get(cls, idx):
        if idx in cls.id_to_mat:
            return cls.id_to_mat[idx]

    @staticmethod
    def find_links(recipe):
        for string in recipe:
            if type(string) is not str:
                continue
            if "tbc.wowhead.com" in string:
                yield string

    @staticmethod
    def get_id_mat(link):
        sep = link.split('/')
        try:
            return int(sep[-2][5:]), sep[-1].replace('-', ' ').replace('rs ', "r's ")
        except (IndexError, ValueError) as e:
            print(sep)
            print(e)