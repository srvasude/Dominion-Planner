from Card import Card, singleton
'''
    Action Card:
        +2 Actions
        +2 Coins
        +1 Buy
'''
@singleton
class Festival(Card):
    def __init__(self):
        Card.__init__(self, name='Festival', cost=5, action=fest)

def fest(gameState):
    gameState = gameState.clone()
    abc = gameState.abcs[gameState.turn]
    abc['actions'] += 2
    abc['coins'] += 2
    abc['buys'] += 1
    return gameState
