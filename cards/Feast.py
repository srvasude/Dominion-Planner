from Card import Card, singleton
from engine.InputSets import InputSets
'''
    Action Card:
        Trash this card. Gain a card costing up to 5 coins.
'''
@singleton
class Feast(Card):
    def __init__(self):
        Card.__init__(self, name='Feast', cost=4, action=gainCard)

def gainCard(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSets.stackCardSet(gameState,
        costs=xrange(5)), gameState)
    gameState.trash[self] += 1
    gameState.pcards[gameState.turn].hand[self] -= 1
    gameState.stacks[result] -= 1
    gameState.pcards[gameState.turn].gain(result)
    return gameState
