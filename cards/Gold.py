import Card.py
'''
    Treasure Card:
        +3 Coins
'''
@singleton
class Gold(Card):
    def __init__(self):
        super(Gold, name='Gold', cost='6', coins='3').__init__()
