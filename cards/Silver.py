from Card import Card, singleton
'''
    Treasure card:
        +2 Coins
'''
@singleton
class Silver(Card):
    def __init__(self):
        super(Silver, self).__init__(name='Silver', cost=3, coins=2)
