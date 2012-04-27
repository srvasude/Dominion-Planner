from Card import Card, singleton
'''
    Action Card:
        +4 Cards
        +1 Buy
        Each other player draws a card.
'''
@singleton
class CouncilRoom(Card):
    def __init__():
        super(Card, self).__init__(name='CouncilRoom', cost=5, 
                action=drawCards)

def drawCards(gameState):
    gameState = gameState.clone()
    gameState.pcards[gameState.turn].draw(3)
    gameState.abcs[gameState.turn]['buys'] += 1
    for pcard in pcards:
        pcard.draw(1)
    return gameState
