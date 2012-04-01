def Card(Object):
    def __init__(self, name='None', coins=0, victoryPoints=0,
            action = None, reaction = None):
        self.name = name
        self.coins = coins
        self.victoryPoints = victoryPoints
        self.action = action
        self.reaction = reaction

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not instances:
            instnaces[cls] = cls()
        return instances[cls]
    return getinstance
