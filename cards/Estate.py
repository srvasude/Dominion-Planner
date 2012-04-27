from Card import Card, singleton
'''
    Victory Card:
        +1 Victory Point
'''
@singleton
class Estate(Card):
    def __init__(self):
        Card.__init__(self, name='Estate', cost=2, victoryPoints=1)
