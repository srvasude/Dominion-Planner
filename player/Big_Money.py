from Player import Player
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import Province, Gold, Silver
class Big_Money(Player):
    def selectInput(self, inputs, gameState,actionSimulator=None):
        return inputs[0]
    def playActionPhase(self, gameState):
        return
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        possibleBuys = self.availableBuys(gameState, coins)
        card = None
        if Province.Province() in possibleBuys:
            card = Province.Province()
        elif Gold.Gold() in possibleBuys:
            card = Gold.Gold()
        elif Silver.Silver() in possibleBuys:
            card = Silver.Silver()
        if card:
            gameState.stacks[card]
            gameState.abcs[gameState.turn]['buys'] -= 1
            gameState.abcs[gameState.turn]['coins'] -= card.cost
            gameState.pcards[gameState.turn].gain(card)

    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
    


