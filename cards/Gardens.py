import Card.py
'''
    Victory Card:
        Worth 1 Victory point for every 10 cards in your deck (rounded down)
'''
@singleton
class Gardens(Card):
    def __init__(self):
        super(Gardens, name='Gardens', cost=4, 
                victoryPoints = compute).__init__()

def compute(gameState):
    return gameState[me].cardCount//10

