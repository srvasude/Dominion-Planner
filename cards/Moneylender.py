from Card import Card, singleton
from Copper import Copper
from ..engine.InputSets import InputSets
'''
    Action Card:
        Trash a Copper from your hand. If you do, +3 coins.
'''
@singleton
class Moneylender(Card):
    def __init__():
        super(Card, self).__init__(name="Moneylender", cost="4", action=lend)

def lend(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    if gameState.pcards[gameState.turn][Copper()] > 0:
        result = currentPlayer.selectInput(InputSets.tf(), gameState,
                helpMessage='Do you want to trash a copper?')
        if result:
            gameState.pcards[gameState.turn][Copper()] -= 1
            gameState.trash[Copper()] += 1
            gameState.abcs[gameState.turn]['coins'] += 3
    return gameState
