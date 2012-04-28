class MarkovNode(object):
    def __init__(self, gameState):
        self.state = gameState.clone() 
        self.abcs = self.start.abcs[self.start.turn]
        self.cards = self.start.pcards[self.start.turn]

    def possibleActions(self):
        if self.abcs['actions'] = 0:
            return []
        return filter((lambda x : return x.reward != None), 
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
    def list_successors(self, state, action):
      #Needs to be defined in terms of action simulator 


def value_iteration(

