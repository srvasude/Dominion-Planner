from Card import Card, singleton
'''
    Treasure card:
        +2 Coins
'''
@singleton
class Silver(Card):
    def __init__(self):
        Card.__init__(self, name='Silver', cost=3, coins=2)
