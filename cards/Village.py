from Card import Card, singleton
'''
    Action Card:
        +1 Card
        +2 Actions
'''
@singleton
class Village(Card):
    def __init__(self):
        super(Card, self).__init__(name='Village', cost=3, action=village)

def village(gameState):
    gameState.pcards[gameState.turn].draw(1)
    gameState.abcs[gameState.turn]['actions'] += 2
