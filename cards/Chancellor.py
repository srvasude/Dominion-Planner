from Card import Card, singleton
from engine.InputSets import InputSets
'''
    Action Card:
        +2 Coins
        You may immediately put your deck into your discard pile
'''
@singleton
class Chancellor(Card):
    def __init__(self):
        Card.__init__(self, name='Chancellor', cost=3, action=gainDiscard)

def gainDiscard(gameState):
    gameState = gameState.clone()
    gameState.abcs[gameState.turn]['coins'] += 2
    currentPlayer = gameState.players[gameState.turn]
    response = currentPlayer.selectInput(InputSets.tf(), gameState, actionSimulator = actionSim)
    if response and response[0]:
        gameState.pcards[gameState.turn].deckToDiscard()
    return gameState

def actionSim(gameState, response):
    gameState = gameState.clone()
    if response:
        gameState.pcards[gameState.turn].deckToDiscard()
    return gameState
