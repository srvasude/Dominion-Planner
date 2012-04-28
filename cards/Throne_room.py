from Card import Card, singleton
from engine.InputSets import InputSets
'''
    Action Card:
        Choose any Action card in your hand. Play it twice.
'''
@singleton
class Throne_room(Card):
    def __init__(self):
        Card.__init__(self, name='ThroneRoom', cost=4, action=dbl)

def dbl(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSets.handCardSet(gameState, 1, filtered = lambda c: (c.action != None)),
            gameState, actionSimulator=dblSimulator, helpMessage='Choose which card to play twice')
    if result == None:
        return gameState
    else:
        result = result[0]
    gameState.pcards[gameState.turn].playFromHand(result)
    gameState = result.action(gameState)
    gameState = result.action(gameState)
    return gameState
    
def dblSimulator(gameState, inputValue):
    gameState = gameState.clone()
    result = inputValue
    if result == None:
        return gameState
    else:
        result = result[0]
    gameState.pcards[gameState.turn].playFromHand(result)
    gameState = result.action(gameState)
    gameState = result.action(gameState)
    return gameState
