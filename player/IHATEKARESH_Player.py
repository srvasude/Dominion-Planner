from Player import Player
from sys import stdin

class IHATEKARESH_Player(Player):
    def setParams(self, params, cvparams, goalDeck):
        self.params = params
        self.goalDeck = goalDeck
        self.cvparams = cvparams
    def evaluate(self, gameState):
        abcs = gameState.abcs[gameState.turn]
        total_coins = abcs['coins'] + self.totalTreasure(gameState)
        return (abcs['actions']*self.params[0] + abcs['buys']*self.params[1] 
                + total_coins * self.params[2] + total_coins/(abcs['buys'] + 1)
                * self.params[3])
                
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        inputs = list(inputs)
        if not inputs:
            return None
        inputs_value = ((sum((self.evaluate(actionSimulator(gs, i)) for trial in xrange(10)))/10, i) for i in inputs) 
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
        while self.availableActions(gameState):
            choice = None
            v = self.evaluate(gameState)
            mdp = MarkovDecisionProcess(gs, None, self.evaluate, cutOff = 2).run()
            if (mpd[0] > v):
                choice = mdp[1]
            if not choice:
                break
            else:
                choice = choice[0]
                print 'Play: ' + choice.name
                gameState.pcards[gameState.turn].discardFromHand(choice)
                gameState.abcs[gameState.turn]['actions'] -= 1
                gameState = choice.action(gameState)
        return gameState
        
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        abcs = gameState.abcs[gameState.turn]
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        cards = gameState.pcards[gameState.turn] 
        cards_to_buy = deck - cards.allCards()
        while abcs['buys'] > 0:
            possibleBuys = self.availableBuys(gameState, coins)
            if not possibleBuys:
                break
            value_buys = ((self.valueCard(gameState, c), c) for c in possibleBuys)
            buy = max(value_buys)[1]
            gameState.stacks[buy] -= 1
            buys -= 1
            coins -= buy.cost
            gameState.pcards[gameState.turn].gain(buy)
            if buy in self.goalDeck:
                cards_to_buy[buy] -= 1
        gameState.abcs[gameState.turn]['buys'] = buys
        gameState.abcs[gameState.turn]['coins'] = coins
        return gameState
        
    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
    
    def valueCard(self, gameState, card, cards_to_buy):
        towards_goal_deck = int(card in cards_to_buy)
        num_left = gameState.stacks[card]

        return self.paramscard.cost

