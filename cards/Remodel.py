from Card import Card, singleton
import InputSet
'''
    Action Card:
        Trash a card from your hand. Gain a card costing up to 2 coins more
        than the trashed card
'''
@singleton
class Remodel(Card):
    def __init__():
        super(Card, self).__init__(name="Remodel", cost="4", action=remod)

def remod(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSet.handCardSet(gameState, 1),
            gameState)
    cards = gameState.pcard[gameState.turn]
    cards.hand[result] -= 1
    gameState.trash[result] += 1
    costs = [result.cost + i for i in xrange(2)] 
    result = currentPlayer.selectInput(InputSet.stackCardSet(gameState, costs=costs), gameState)
    gameState.stacks[result] -= 1
    cards.gain(result)
    return gameState
