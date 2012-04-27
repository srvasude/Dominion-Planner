from Card import Card, singleton
'''
    Treasure Card:
        +3 Coins
'''
@singleton
class Gold(Card):
    def __init__(self):
        Card.__init__(self, name='Gold', cost=6, coins=3)
