from Card import Card, singleton
'''
    Victory Card:
        +1 Victory Point
'''
@singleton
class Estate(Card):
    def __init__(self):
        super(Estate, self).__init__(name='Estate', cost=2,
                victoryPoints=1)
