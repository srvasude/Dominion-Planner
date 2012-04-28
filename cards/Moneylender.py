from Card import Card, singleton
from Copper import Copper
from engine.InputSets import InputSets
'''
    Action Card:
        Trash a Copper from your hand. If you do, +3 coins.
'''
@singleton
class Moneylender(Card):
    def __init__(self):
        Card.__init__(self, name="Moneylender", cost=4, action=lend)

def lend(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    if gameState.pcards[gameState.turn].hand[Copper()] > 0:
        result = currentPlayer.selectInput(InputSets.tf(), gameState, actionSimulator = actionSim,
                helpMessage='Do you want to trash a copper?')
        if result:
            gameState.pcards[gameState.turn].hand[Copper()] -= 1
            gameState.trash[Copper()] += 1
            gameState.abcs[gameState.turn]['coins'] += 3
    return gameState

def actionSim(gameState, result):
    gameState = gameState.clone()
    if result:
            gameState.pcards[gameState.turn].hand[Copper()] -= 1
            gameState.trash[Copper()] += 1
            gameState.abcs[gameState.turn]['coins'] += 3
    return gameState
