from Card import Card, singleton
'''
    Action Card:
        +3 cards
'''
@singleton
class Smithy(Card):
    def __init__(self):
        super(Card, self).__init__(name='Smithy', cost=4, action=smith)

def smith(gameState):
    gameState.pcards[gameState.turn].draw(3)
