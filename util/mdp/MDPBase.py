class MarkovDecisionProcess(Object):
    def __init__(self, gameState, discount, rewardHeuristic):
        
        self.start = {'cards': gameState.pcards[gameState.turn]}
        self.start.update(gameState.abcs[gameState.turn])
        self.start.update({'stacks':gameState.stacks})
        self.discount = discount
        self.reward = rewardHeuristic

    def possibleActions(self, state):
        if state['actions'] = 0:
            return []
        return filter((lambda x : return x.reward != None), 
                (for card in state['cards'].hand))

    def doAction(
    

