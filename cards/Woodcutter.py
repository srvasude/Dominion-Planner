from Card import Card, singleton
'''
    Action Card:
        +1 Buy
        +2 Coins
'''
@singleton
class Woodcutter(Card):
    def __init__():
        super(Card, self).__init__(name='Woodcutter', cost=3, 
                action=cutwood)

def cutwood(gameState):
    abc = gameState.abcs[gameState.turn]
    abc['buys'] += 1
    abc['coins'] += 2
