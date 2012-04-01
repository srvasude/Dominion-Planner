import Card.py
'''
    Treasure card:
        +2 Coins
'''
@singleton
class Silver(Card):
    def __init__(self):
        super(Silver, name='Silver', cost=3, coins=2).__init__()
