from Card import Card, singleton
from engine.InputSets import InputSets
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
        Card.__init__(self, name='Mine', cost=5, action=mine)

def mine(gameState):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    minedCard = currentPlayer.selectInput(
            InputSets.handCardSet(gameState, 1, 
            filtered=(lambda x: x.coins > 0)), gameState, actionSimulator = mineSim1,
            helpMessage = 'Which Treasure do you choose to Trash?')
    if minedCard == None:
        return gameState
    else:
        minedCard = minedCard[0]
    costs = [minedCard.cost + i for i in xrange(4)]
    gameState.trash[minedCard] += 1
    gameState.pcards[gameState.turn].hand[minedCard] -= 1
    newCard = currentPlayer.selectInput(
            InputSets.stackCardSet(gameState, 1, costs=costs,
                filtered=(lambda x: x.coins > 0)), gameState, actionSimulator = mineSim2,)
    if newCard == None:
        return gameState
    else:
        newCard = newCard[0]
    gameState.stacks[newCard] -= 1
    gameState.pcards[gameState.turn].hand[newCard] += 1
    return gameState

def mineSim1(gameState, minedCard):
    gameState = gameState.clone()
    currentPlayer = gameState.players[gameState.turn]
    if minedCard == None:
        return gameState
    else:
        minedCard = minedCard[0]
    costs = [minedCard.cost + i for i in xrange(4)]
    gameState.trash[minedCard] += 1
    gameState.pcards[gameState.turn].hand[minedCard] -= 1
    newCard = currentPlayer.selectInput(
            InputSets.stackCardSet(gameState, 1, costs=costs,
                filtered=(lambda x: x.coins > 0)), gameState)
    if newCard == None:
        return gameState
    else:
        newCard = newCard[0]
    gameState.stacks[newCard] -= 1
    gameState.pcards[gameState.turn].hand[newCard] += 1
    return gameState

def mineSim2(gameState, newCard):
    gameState = gameState.clone()
    if newCard == None:
        return gameState
    else:
        newCard = newCard[0]
    gameState.stacks[newCard] -= 1
    gameState.pcards[gameState.turn].hand[newCard] += 1
    return gameState

