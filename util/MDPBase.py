import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from engine.GameState import GameState
class MarkovNode(object):
    def __init__(self, gameState):
        self.state = gameState.clone() 
        self.abcs = self.state.abcs[self.state.turn]
        self.cards = self.state.pcards[self.state.turn]
    
    def possibleActions(self):
        if self.abcs['actions'] == 0:
            return []
        return filter((lambda x : x.action != None), self.cards.hand.keys())
    
    def applyAction(self, action_card):
        if self.abcs['actions'] == 0:
            return self
        else:
            state = self.state.clone()
            state.pcards[state.turn].playFromHand(action_card)
            state.abcs[state.turn]['actions'] -= 1
            return MarkovNode(action_card.action(state))

class MarkovDecisionProcess(object):
    def  __init__(self, gameState, rewardHeuristic, discount=1, cutOff=1):
        self.start = MarkovNode(gameState)
        self.discount = discount
        self.reward = rewardHeuristic
        self.cutOff = cutOff
            
    '''
        returns a tuple of the form (bestAExpectedValue, (bestACard_tuple), state)
    '''
    def run(self):
        return self.recrun(self.start, self.cutOff)
    def recrun(self, mnode, n):
        if n == 0 or mnode.abcs['actions'] == 0:
            return (self.reward(mnode.state), (), mnode.state)
        acards = mnode.possibleActions()
        if not acards:
            return (self.reward(mnode.state), (), mnode.state)
        else:
            bestA = max( ((self.recrun(mnode.applyAction(acard), n-1), acard) for acard in acards) )
            transitionValue = self.reward(bestA[0][2])-self.reward(mnode.state)
            bestA = ((transitionValue + self.discount * bestA[0][0]), (bestA[1], ) + bestA[0][1], mnode.state)
            return bestA
    '''
    def recrun(self, mnode, n):
        if n == 0 or mnode.abcs['actions'] == 0:
            return (self.reward(mnode.state), ())
        acards = mnode.possibleActions()
        if not acards:
            return (self.reward(mnode.state), ())
        else:
            bestA = max( ((self.recrun(mnode.applyAction(acard), n-1), acard) for acard in acards) )
            bestA = ((self.reward(mnode.state) + self.discount * bestA[0][0])/(1 + self.discount), (bestA[1], ) + bestA[0][1])
            return bestA
    '''
    

