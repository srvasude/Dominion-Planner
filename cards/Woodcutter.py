from Card import Card, singleton
'''
    Action Card:
        +1 Buy
        +2 Coins
'''
@singleton
class Woodcutter(Card):
    def __init__(self):
        Card.__init__(self, name='Woodcutter', cost=3, 
                action=cutwood)

def cutwood(gameState):
    gameState = gameState.clone()
    abc = gameState.abcs[gameState.turn]
    abc['buys'] += 1
    abc['coins'] += 2
    return gameState
