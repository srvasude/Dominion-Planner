import Card.py
'''
    Action Card:
        Trash this card. Gain a card costing up to 5 coins.
'''
class Feast(Card):
    def __init__(self):
        super(Feast, name='Feast', cost=4, action = gainCard)

def gainCard(gameState):
    cardToChoose = InputClass.getSetInputs()
