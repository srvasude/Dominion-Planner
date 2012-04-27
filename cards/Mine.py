from Card import Card, singleton
from ..engine.InputSets import InputSets
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
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    minedCard = currentPlayer.selectInput(
            InputSets.handCardSet(gameState, 1, 
            filtered=(lambda x: x.coins > 0)), gameState,
            helpMessage = 'Which Treasure do you choose to Trash?')
    costs = [minedCard.cost + i for i in xrange(4)]
    gameState.trash[minedCard] += 1
    gameState.pcards[gameState.turn][minedCard] -= 1
    newCard = currentPlayer.selectInput(
            InputSets.stackCardSet(gameState, 1, costs=costs,
                filtered=(lambda x: x.coins > 0)), gameState)
    gameState.stacks[newCard] -= 1
    gameState.pcards[gameState.turn][newCard] += 1
    return gameState
