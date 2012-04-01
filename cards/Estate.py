import Card.py
'''
    Victory Card:
        +1 Victory Point
'''
@singleton
def Estate(Card):
    def __init__(self):
        super(Estate, name='Estate', cost=2, victoryPoints=1).__init__()
