from Player import Player
from sys import stdin
from util.MDPBase import MarkovDecisionProcess
from cards import *
from engine.InputSets import InputSets

class GeneticDeckHelper(Player):
    def __init__(self, params):
        self.params = params
        self.mdpDiscount = 1
    
    def evaluate(self, gameState):
        abcs = gameState.abcs[gameState.turn]
        total_coins = abcs['coins'] + sum([card.coins*gameState.pcards[0].hand[card] for card in gameState.pcards[0].hand])
        v = [0,0,0,0,0]
        v[0] = abcs['actions'] * len(list(InputSets.handCardSet(gameState, number=1, filtered = lambda c: (c.action != None))))
        v[1] = min(abcs['buys']*8, total_coins)
        v[2] = total_coins
        v[3] = sum([c.cost*n for c,n in gameState.pcards[gameState.turn].allCards().items()])
        v[4] = (gameState.pcards[gameState.turn].currInPlay.count + gameState.pcards[gameState.turn].hand.count)
        return sum([v[i]*self.params[i] for i in xrange(len(self.params))])
                
    def selectInput(self, inputs, gameState, actionSimulator=None, helpMessage=None):
        m = -1
        choice = None
        inputs = list(inputs)
        for i in inputs:
            temp = 0
            if actionSimulator != None:
                for x in xrange(3):
                    gs = actionSimulator(gameState, i)
                    temp += MarkovDecisionProcess(gs, self.evaluate, discount = self.mdpDiscount, cutOff = 0).run()[0]
            if temp > m:
                m = temp
                choice = tuple(i)
        return choice
        '''
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
        '''    
    
    def playActionPhase(self, gameState):
        gameState = gameState.clone()
        while self.availableActions(gameState):
            choice = None
            v = self.evaluate(gameState)
            mdp = MarkovDecisionProcess(gameState, self.evaluate, discount = self.mdpDiscount, cutOff = 3).run()
            choice = mdp[1]
            if not choice:
                break
            else:
                choice = choice[0]
                gameState.pcards[gameState.turn].playFromHand(choice)
                gameState.abcs[gameState.turn]['actions'] -= 1
                gameState = choice.action(gameState)
        return gameState
        
    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        return gameState
        
    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
    
    def valueCard(self, gameState, card, cards_to_buy):
        return card.cost
    

