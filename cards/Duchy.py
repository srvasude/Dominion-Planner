import Card.py
'''
    Victory Card:
        +3 Victory Points
'''
@singleton
def Duchy(Card):
    def __init__(self):
        super(Duchy, name='Duchy', cost=5, victoryPoints=3)
