from Card import Card, singleton
'''
    Action Card:
        Trash a Treasure card from your hand. Gain a Treasure card costing
        up to 3 coins more; put it into your hand.
'''
'''
state.players, state.pcards, state.turn, state.stacks
'''
@singleton
class Mine(Card):
    def __init__(self):
        super(Mine, self).__init__(name='Mine', cost=5, action=mine)

def mine(gameState):
    currentPlayer = gameState.players[gameState.turn]
    minedCard = currentPlayer.selectInput(InputSets.
    gameState.currentPlayer
