class Player:
    def selectInput(self, inputs, gameState, actionSimulator=None):
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
        return InputSets.handCardSet(gameState, 1, labmda c: (c.action != None))

    def totalTreasure(self, gameState):
        hand = gameState.pcards[gameState.turn].hand
        total = 0
        for card in hand:
            total += card.coins
        return total
