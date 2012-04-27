from Card import Card, singleton
'''
    Victory Card:
        +3 Victory Points
'''
@singleton
class Duchy(Card):
    def __init__(self):
        Card.__init__(self, name='Duchy', cost=5, victoryPoints=3)
