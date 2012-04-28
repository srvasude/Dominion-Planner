class MarkovNode(object):
    def __init__(self, gameState):
        self.state = gameState.clone() 
        self.abcs = self.state.abcs[self.start.turn]
        self.cards = self.state.pcards[self.start.turn]
    
    def possibleActions(self):
        if self.abcs['actions'] = 0:
            return []
        return filter((lambda x : x.action != None), 
                (for card in self.cards.hand))
    
    def applyAction(self, action_card):
        if self.abcs['actions'] == 0:
            return self
        else:
            state = self.state.clone()
            state.pcards[state.turn].discardFromHand(action_card)
            state.abcs[state.turn]['actions'] -= 1
            return MarkovNode(action_card.action(state))
    

class MarkovDecisionProcess(object):
    def  __init__(self, gameState, discount, 
            rewardHeuristic, cutOff=1):
        self.start = MarkovNode(gameState)
        self.discount = discount
        self.reward = rewardHeuristic
        self.cutOff = cutOff
            
    '''
        returns a tuple of the form (bestAExpectedValue, (bestACard_tuple))
    '''
    def run(self, mnode = self.start, n = self.cutOff):
        if n == 0 or mnode.abcs['actions'] == 0:
            return (self.rewardHeuristic(mnode.state), ())
        acards = mnode.possibleActions()
        if not acards:
            return return (self.rewardHeuristic(mnode.state), ())
        else:
            bestA = max( (self.run(mnode=mnode.applyAction(acard), n=n-1), acard) for acard in acards) )
            bestA = (bestA[0][0], bestA[1] + bestA[0][1])
            return bestA
    
