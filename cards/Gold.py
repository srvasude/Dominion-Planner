from Card import Card, singleton
'''
    Treasure Card:
        +3 Coins
'''
@singleton
class Gold(Card):
    def __init__(self):
        super(Gold, self).__init__(name='Gold', cost='6', coins='3')
