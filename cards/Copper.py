from Card import Card, singleton
'''
    Treasure Card:
        +1 Coin
'''
@singleton
class Copper(Card):
    def __init__(self):
        super(Copper, self).__init__(name='Copper', coins=1)
