def Card(Object):
    def __init__(self, name='None', coins=0, victoryPoints=0):
        self.name = name
        self.coins = coins
        self.victoryPoints = victoryPoints
    def doAction(self, gameState, **kwargs):
        raise UnsupportedException() 
    def hValue(self, gameState):
        raise UnsupportedException()
