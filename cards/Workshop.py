from Card import Card, singleton
from engine.InputSets import InputSets
'''
    Action Card:
        Gain a card costing up to 4 coins
'''
@singleton
class Workshop(Card):
    def __init__(self):
        Card.__init__(self, name="Workshop", cost="3", action=work)

def work(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSets.stackCardSet(gameState, 
        costs=[4]),gameState)
    gameState.stacks[result] -= 1
    gameState.pcards[gameState.turn].gain(result)
    return gameState
    
