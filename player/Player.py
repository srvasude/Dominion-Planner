class Player:
    def selectInput(self, inputs, gameState, actionSimulator=None):
        return NotImplemented()
    
    def playActionPhase(self, gameState):
        return NotImplemented()
    
    def playBuyPhase(self, gameState):
        return NotImplemented()
    
    def valueCard(self, gameState, card):
        return NotImplemented()
    
