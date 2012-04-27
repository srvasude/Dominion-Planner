from Card import Card, singleton
'''
    Action Card:
        +2 Cards
        +1 Action
'''
@singleton
class Laboratory(Card):
    def __init__(self):
        Card.__init__(self, name='Laboratory', cost=5, action=lab)
def lab(gameState):
    gameState = gameState.clone()
    gameState.pcards[gameState.turn].draw(2)
    gameState.abcs[gameState.turn]['actions'] += 1
    return gameState
