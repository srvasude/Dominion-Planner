from Card import Card, singleton
from ..engine.InputSets import InputSets
'''
    Action Card:
        Choose any Action card in your hand. Play it twice.
'''
@singleton
class ThroneRoom(Card):
    def __init__(self):
        super(Card, self).__init__(name='ThroneRoom', cost=4, action=dbl)

def dbl(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSets.handCardSet(gameState, 1),
            gameState, helpMessage='Choose which card to play twice')
    result.action(gameState)
    result.action(gameState)
    return gameState
