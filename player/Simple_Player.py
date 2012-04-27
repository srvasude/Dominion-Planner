from Player import Player
class Simple_Player(Player):
    def evaluate(self, gameState):
        return (gameState.abcs[gameState.turn]['actions'] 
              + gameState.abcs[gameState.turn]['buys']
              + gameState.abcs[gameState.turn]['coins']
              + self.totalTreasure(gameState))
                
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        m = -1
        choice = None
        for i in inputs:
            temp = (self.evaluate(actionSimulator(gs, i)) + evaluate(actionSimulator(gs, i))) / 2.0
            if temp > m:
                m = temp
                choice = i
        return choice
    
    def playActionPhase(self, gameState):
        gameState = gameState.clone()
        actions = self.availableActions(gameState)
        while len(actions) > 0:
            choice = None
            v = self.evaluate(gameState)
            for a in actions:
                tempv = self.evaluate(a.action(gs))
                if tempv >= v:
                    choice = a
                    v = tempv
            if not choice:
                break
            else:
                gameState.pcards[gameState.turn].discardFromHand(choice)
                gameState.abcs[gameState.turn]['actions'] -= 1
                gameState = choice.action(gameState)
                actions = self.availableActions(gameState)
        return gameState
    
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        buys = gameState.abcs[gameState.turn]['buys']
        coins = gameState.abcs[gameState.turn]['coins'] 
        + self.totalTreasure(gameState)
        while buys > 0:
            m = -1
            buy = None
            possibleBuys = self.availableBuys(gameState, coins)
            for c in possibleBuys:
                if self.valueCard(gameState, c) > m:
                    m = self.valueCard(gameState, c)
                    buy = c
            if not buy:
                break
            else:
                gameState.stacks[buy] -= 1
                buys -= 1
                coins -= buy.cost
                gameState.pcards[gameState.turn].gain(buy)
        gameState.abcs[gameState.turn]['buys'] = buys
        gameState.abcs[gameState.turn]['coins'] = coins
        return gameState
        
    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
    
    def valueCard(self, gameState, card):
        return card.cost

