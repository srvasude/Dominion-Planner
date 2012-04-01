import Card.py
'''
    Treasure Card:
        +1 Coin
'''
@singleton
class Copper(Card):
    def __init__(self):
        super(Copper, name='Copper', cost=0, coins=1).__init__()
