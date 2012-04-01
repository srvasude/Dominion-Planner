from Card import Card, singleton
'''
    Victory Card:
        +3 Victory Points
'''
@singleton
class Duchy(Card):
    def __init__(self):
        super(Duchy, self).__init__(name='Duchy', cost=5, victoryPoints=3)
