from Player import Player
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import Province, Gold, Silver, Estate, Duchy
class Big_Money_Ultimate(Player):
    def selectInput(self, inputs, gameState,actionSimulator=None):
        return inputs[0]
    def playActionPhase(self, gameState):
        return
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        possibleBuys = self.availableBuys(gameState, coins)
        card = None
        prvnce = Province.Province()
        if prvnce in possibleBuys:
            card = prvnce
        elif Duchy.Duchy() in possibleBuys and gameState.stacks[prvnce] <= 5
            card = Duchy.Duchy()
        elif Estate.Estate() in possibleBuys and gameState.stacks[prvnce] <= 2 
            card = Estate.Estate()
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
    


