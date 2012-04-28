from Player import Player
from sys import stdin

class IHATEKARESH_Player(Player):
    def setParams(self, params, goalDeck):
        self.params = params
        self.goalDeck = goalDeck
        
    def evaluate(self, gameState):
        abcs = gameState.abcs[gameState.turn]
        total_coins = abcs['coins'] + self.totalTreasure(gameState)
        return abcs['actions']*self.params[0] + abcs['buys']*self.params[1] 
                + total_coins * params[2] + total_coins/(abcs['buys'] + 1)
                * params[3]
                
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        inputs = list(inputs)
        if not inputs:
            return None
        inputs_value = ((sum(self.evaluate(actionSimulator(gs, i)) for xrange(10))/10, i) for i in inputs) 
        return max(inputs_value)[1]
    ''' YOUR WAY
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
    '''
    
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
        gameState = gameState.clone()
        buys = gameState.abcs[gameState.turn]['buys']
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        ca
        while buys > 0:
            m = -1
            buy = None
            possibleBuys = self.availableBuys(gameState, coins)
            if not possibleBuys:
                break
            value_buys = ((self.valueCard(gameState, c), c) for c in possibleBuys)
            buy = max(value_buys)[1]
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
        deck = self.goalDeck
        cards = gameState.pcards[gameState.turn]
        current_deck = cards.hand + cards.discard + cards.deck + cards.currInPlay 
        cards_to_buy = deck - current_deck
        return card.cost

