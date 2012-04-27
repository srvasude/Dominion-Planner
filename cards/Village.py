from Card import Card, singleton
'''
    Action Card:
        +1 Card
        +2 Actions
'''
@singleton
class Village(Card):
    def __init__(self):
        Card.__init__(self, name='Village', cost=3, action=village)

def village(gameState):
    gameState = gameState.clone()
    gameState.pcards[gameState.turn].draw(1)
    gameState.abcs[gameState.turn]['actions'] += 2
    return gameState
