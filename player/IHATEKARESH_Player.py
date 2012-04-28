from Player import Player
from sys import stdin
from util.MDPBase import MarkovDecisionProcess
from cards import *

class IHATEKARESH_Player(Player):
    def __init__(self, stacks, startDeck):
        self._makingAction = False
        self.setParams((1,10,3,0,5), (), stacks+startDeck)
    
    def setParams(self, params, cvparams, goalDeck):
        self.params = params
        self.goalDeck = goalDeck
        self.cvparams = cvparams
    
    def evaluate(self, gameState):
        abcs = gameState.abcs[gameState.turn]
        total_coins = abcs['coins'] + self.totalTreasure(gameState)
        v = [0,0,0,0,0]
        v[0] = self.params[0] * abcs['actions'] * len(self.availableActions(gameState))
        v[1] = self.params[1] * min(abcs['buys'], 1+total_coins/5) * total_coins
        v[2] = self.params[2] * total_coins
        v[3] = self.params[3] * sum([c.cost*n for c,n in gameState.pcards[gameState.turn].allCards().items()])
        v[4] = self.params[4] * (gameState.pcards[gameState.turn].currInPlay.count + gameState.pcards[gameState.turn].hand.count)
        return sum(v)
                
    def selectInput(self, inputs, gameState, actionSimulator=None, helpMessage=None):
        _makingAction = self._makingAction
        self._makingAction = False
        inputs = list(inputs)
        if (not inputs) or (not actionSimulator):
            selectedInput = None
        else:
            inputs_value = ((sum((self.evaluate(actionSimulator(gameState, i)) for trial in xrange(5)))/5, i) for i in inputs) 
            selectedInput = max(inputs_value)[1]
        if _makingAction:
            self._makingAction = True
            if hasattr(selectedInput, '__iter__'):
                print '(' + selectedInput[0].name + ')',
            else:
                print '(' + str(selectedInput) + ')',
        return selectedInput
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
            mdp1 = MarkovDecisionProcess(gameState, self.evaluate, discount = .7, cutOff = 1).run()
            mdp2 = MarkovDecisionProcess(gameState, self.evaluate, discount = .7, cutOff = 2).run()
            mdp3 = MarkovDecisionProcess(gameState, self.evaluate, discount = .7, cutOff = 3).run()
            mdp4 = MarkovDecisionProcess(gameState, self.evaluate, discount = .7, cutOff = 4).run()
            mdp5 = MarkovDecisionProcess(gameState, self.evaluate, discount = .7, cutOff = 5).run()
            print v, mdp2#debug
            print v, mdp3#debug
            print v, mdp4#debug
            print v, mdp5#debug
            #print 't1', MarkovDecisionProcess(gameState, None, self.evaluate, cutOff = 2).run()#debug
            #print 't2', MarkovDecisionProcess(gameState, None, self.evaluate, cutOff = 1).run()#debug
            #print': {', str(gameState.pcards[gameState.turn].deck), '} | {', str(gameState.pcards[gameState.turn].deck+gameState.pcards[gameState.turn].discard), '}'#debug
            if (mdp1[0] > v):
                choice = mdp1[1]
                
            if mdp1[1][0]==mdp3[1][0] or mdp1[1][0]==mdp5[1][0]:
                choice = mdp1[1]
            else:
                choice = mdp5[1]
            print 'Choice:', choice[0].name, ' (' , mdp1[1][0].name, mdp3[1][0].name, mdp5[1][0].name, ')'
            if not choice:
                break
            else:
                choice = choice[0]
                print 'Play: ' + choice.name,
                gameState.pcards[gameState.turn].playFromHand(choice)
                gameState.abcs[gameState.turn]['actions'] -= 1
                self._makingAction = True
                gameState = choice.action(gameState)
                self._makingAction = False
                print '\n\t' + str(gameState.abcs[gameState.turn])
                print '\thand: ' + str(gameState.pcards[gameState.turn].hand)
        return gameState
        
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        abcs = gameState.abcs[gameState.turn]
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        cards = gameState.pcards[gameState.turn] 
        cards_to_buy = self.goalDeck - cards.allCards()
        while abcs['buys'] > 0:
            possibleBuys = self.availableBuys(gameState, coins)
            if not possibleBuys:
                break
            value_buys = ((self.valueCard(gameState, c, cards_to_buy), c) for c in possibleBuys)
            maxBuy = max(value_buys)
            if maxBuy[0] < 0:
                break;
            buy = maxBuy[1]
            gameState.stacks[buy] -= 1
            abcs['buys'] -= 1
            coins -= buy.cost
            gameState.pcards[gameState.turn].gain(buy)
            if buy in self.goalDeck:
                cards_to_buy[buy] -= 1
        gameState.abcs[gameState.turn]['coins'] = coins
        return gameState
        
    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
    
    def valueCard(self, gameState, card, cards_to_buy):
        towards_goal_deck = int(card in cards_to_buy)
        num_left = gameState.stacks[card]
        card_amount = cards_to_buy[card]
        in_goal_deck = towards_goal_deck*self.cvparams[0] + card_amount*self.cvparams[1]
        
        return card.cost*self.cvparams[2] + in_goal_deck
        '''if card==Province.Province() and (gameState.abcs[gameState.turn]['coins']>=11):
            return 10000000
        if (card.victoryPoints or card==Copper.Copper() or (card==Silver.Silver() and gameState.pcards[0].allCards()[Silver.Silver()]>4)):
            return -2
        if card==Gold.Gold() and gameState.pcards[0].allCards()[Gold.Gold()]<gameState.pcards[0].allCards()[Market.Market()]:
            return 1000000
        if card==Laboratory.Laboratory():
            return 10000*gameState.stacks[card]
        if card.cost==5:
            return 10000*gameState.stacks[card]
        return self.params[0]*card.cost '''

