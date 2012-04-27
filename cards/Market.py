from Card import Card, singleton
'''
    Action Card:
        +1 Card
        +1 Action
        +1 Buy
        +1 Coin
'''
@singleton
class Market(Card):
    def __init__(self):
        Card.__init__(self, name='Market', cost=5, action=market)

def market(gameState):
    gameState = gameState.clone()
    gameState.pcards[gameState.turn].draw(1)
    abc = gameState.abcs[gameState.turn]
    for key in abc:
        abc[key] += 1
    return gameState
