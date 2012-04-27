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
        return InputSets.handCardSet(gameState, number=1, 
            filtered=(lambda c: (c.action != None)))

    def availableBuys(self, gameState, money):
        if not gameState.abcs[gameState.turn]['buys']:
            return []
        return InputSet.stackCardSet(gameState, number=1, 
            costs=range(money+1))
    def totalTreasure(gameState):
        hand = gameState.pcards[gameState.turn].hand
        total = 0
        for card in hand:
            total += card.coins
        return total
