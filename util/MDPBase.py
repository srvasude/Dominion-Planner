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
            return MarkovNode(action_card.action(self.state))
    

class MarkovDecisionProcess(object):
    def  __init__(self, gameState, discount, 
            rewardHeuristic, cutOff=1):
        self.start = MarkovNode(gameState)
        self.discount = discount
        self.reward = rewardHeuristic
        self.cutOff = cutOff
    
    '''
        returns the tuple with the higher expected utility.
        a1 and a2 are tuples of the form:
        (action_card, expected_utility_of_playing_action_card)
    '''
    def _maxA(a1, a2):
        if (a1[1] >= a2[1]):
            return a1
        else:
            return a2
            
    '''
        returns a tuple of the form ((bestACard_tuple), bestAExpectedValue)
    '''
    def run(self, mnode = self.start, n = self.cutOff):
        if n == 0 or mnode.abcs['actions'] == 0:
            return ((), self.rewardHeuristic(mnode.state))
        bestA = ((), -1)
        for acard in mnode.possibleActions():
            curA = self.run(mnode=mnode.applyAction(acard), n=n-1)
            curA = ((acard, ) + cur[0], curA[1])
            bestA = _maxA(bestA, curA)
        if bestA[1] == -1:
            return ((), self.rewardHeuristic(mnode.state))
        else:
            return bestA
    
