from Card import Card, singleton
from engine.InputSets import InputSets
'''
    Action Card:
        Trash a card from your hand. Gain a card costing up to 2 coins more
        than the trashed card
'''
@singleton
class Remodel(Card):
    def __init__(self):
        Card.__init__(self, name="Remodel", cost=4, action=remod)

def remod(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    result = currentPlayer.selectInput(InputSets.handCardSet(gameState, 1),
            gameState, actionSimulator = remodSim1, helpMessage='Choose a card to trash')
    if result == None:
        return gameState
    else:
        result = result[0]
    cards = gameState.pcards[gameState.turn]
    cards.hand[result] -= 1
    gameState.trash[result] += 1
    costs = range(result.cost + 2 + 1)
    result = currentPlayer.selectInput(InputSets.stackCardSet(gameState, costs=costs), gameState, actionSimulator = remodSim2)
    if result == None:
        return gameState
    else:
        result = result[0]
    gameState.stacks[result] -= 1
    cards.gain(result)
    return gameState

def remodSim1(gameState, result):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    if result == None:
        return gameState
    else:
        result = result[0]
    cards = gameState.pcards[gameState.turn]
    cards.hand[result] -= 1
    gameState.trash[result] += 1
    costs = range(result.cost + 2 + 1)
    result = currentPlayer.selectInput(InputSets.stackCardSet(gameState, costs=costs), gameState, actionSimulator = remodSim2)
    if result == None:
        return gameState
    else:
        result = result[0]
    gameState.stacks[result] -= 1
    cards.gain(result)
    return gameState

def remodSim2(gameState, result):
    gameState = gameState.clone()
    if result == None:
        return gameState
    else:
        result = result[0]
    gameState.stacks[result] -= 1
    gameState.pcards[gameState.turn].gain(result)
    return gameState

