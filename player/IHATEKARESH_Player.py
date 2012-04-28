from Player import Player
from sys import stdin

class IHATEKARESH_Player(Player):
    def evaluate(self, gameState):
        return (gameState.abcs[gameState.turn]['actions'] * 0
              + gameState.abcs[gameState.turn]['buys']
              + gameState.abcs[gameState.turn]['coins']
              + self.totalTreasure(gameState))
                
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        m = -1
        choice = None
        inputs = list(inputs)
        for i in inputs:
            temp = 0
            if actionSimulator != None:
                gs = actionSimulator(gameState, i)
                #bestStateAfterNMinus1Steps = MDP(gs, N-1)
                #gs = bestStateAfterNMinus1Steps
                temp = self.evaluate(gs)
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
                gs = gameState.clone()
                gs.pcards[gs.turn].discardFromHand(a)
                gs.abcs[gs.turn]['actions'] -= 1
                gs = a.action(gs))
                #MDP should use some caching. maybe.
                #gs = MDP(gs, N-1)
                tempv = self.evaluate(gs)
                if tempv >= v:
                    choice = a
                    v = tempv
            if not choice:
                break
            else:
                print 'Play: ' + choice.name
                gameState.pcards[gameState.turn].discardFromHand(choice)
                gameState.abcs[gameState.turn]['actions'] -= 1
                gameState = choice.action(gameState)
                actions = self.availableActions(gameState)
        return gameState

    def playBuyPhase(self, gameState):
        
