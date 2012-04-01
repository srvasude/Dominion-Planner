import itertools

class InputSets:
    @staticmethod
    def tf():
        return set(True, False)
	
    @staticmethod
    def handCardSet(gameState, number = 'ALL'):
        hand = gameState.pcards[gameState.turn].hand;
        handCards = itertools.chain.from_iterable
                        ((itertools.repeat(c, hand.cards[c]) for c in hand.cards))
        
        if number == 'ALL':
            return itertools.chain.from_iterable
                        ([itertools.combinations(handCards, i) for i in range(hand.size + 1)])
        else:
            return itertools.combinations(handCards, number)
    
    @staticmethod
    def stackCardSet(gameState, number = 1, costs = []):
        stacks = gameState.stacks.keys()
        if costs == []:
            costs = set((c.cost for c in stacks))
        stacks = filter(lambda c: c.cost in costs, stacks)
        return itertools.combinations(stacks, number)
        
