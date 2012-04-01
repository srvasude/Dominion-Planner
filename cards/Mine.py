'''
    Action Card:
        Trash a Treasure card from your hand. Gain a Treasure card costing
        up to 3 coins more; put it into your hand.
'''
@singleton
class Mine(Card):
    def __init__(self):
        super(Mine, name='Mine', cost=5, action = mine)

def mine(gameState):
    requestInput()
    gameState.currentPlayer
