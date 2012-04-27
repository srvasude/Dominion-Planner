from Card import Card, singleton
'''
    Treasure Card:
        +1 Coin
'''
@singleton
class Copper(Card):
    def __init__(self):
        Card.__init__(self, name='Copper', coins=1)
