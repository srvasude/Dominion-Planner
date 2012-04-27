import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
        os.path.pardir)))
from engine.InputSets import InputSets
class Player:
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        return NotImplemented()
    
    def playActionPhase(self, gameState):
        return NotImplemented()
    
    def playBuyPhase(self, gameState):
        return NotImplemented()
        
    def playDiscardPhase(self, gameState):
        return NotImplemented()
    
    def valueCard(self, gameState, card):
        return NotImplemented()

    def availableActions(self, gameState):
        if not gameState.abcs[gameState.turn]['actions']:
            return []
        cards = list(InputSets.handCardSet(gameState, number=1, 
            filtered = lambda c: (c.action != None)))
        return [card[0] for card in cards]

    def availableBuys(self, gameState, money):
        if not gameState.abcs[gameState.turn]['buys']:
            return []
        cards = list(InputSets.stackCardSet(gameState, number=1, 
            costs=range(money+1)))
        return [card[0] for card in cards]
    def totalTreasure(self, gameState):
        hand = gameState.pcards[gameState.turn].hand
        total = 0
        for card in hand:
            total += card.coins
        return total
