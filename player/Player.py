class Player:
    def selectInput(self, inputs, gameState, actionSimulator=None):
        return NotImplemented()
    
    def playActionPhase(self, gameState):
        return NotImplemented()
    
    def playBuyPhase(self, gameState):
        return NotImplemented()
    
    def valueCard(self, gameState, card):
        return NotImplemented()

    def availableActions(self, gameState):
        hand = gameState.pcards[gameState.turn].hand
        if not gameState.abcs[gameState.turn]['actions']:
            return []
        return filter((lambda x : return x.action != None),
                (for card in hand))

    def totalTreasure(self, gameState):
        total = 0
        for card in hand:
            total += card.coins
        return total
