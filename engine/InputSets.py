import itertools
from util.Functions import CardCounts
class InputSets(object):
    '''
        Return True, False choices
    '''
    @staticmethod
    def tf():
        return set(True, False)
	'''
        Return a all combinations of in hand cards.  The number of cards
        in each combination can be set defining number. 
    '''
    @staticmethod
    def handCardSet(gameState, number='ALL',filtered=None):
        hand = gameState.pcards[gameState.turn].hand;
        if filtered:
            hand = CardCounts({k : hand[k] for k in hand if filtered(k)})
        handCards = itertools.chain.from_iterable(
                (itertools.repeat(c, hand[c]) for c in hand))
        
        if number == 'ALL':
            return itertools.chain.from_iterable(
                    [itertools.combinations(handCards, i) 
                    for i in range(hand.size + 1)])
        else:
            return itertools.combinations(handCards, number)
    
    @staticmethod
    def stackCardSet(gameState, number=1, costs=[], filtered=None):
        stacks = gameState.stacks.keys()
        stackNums = gameState.stacks
        if filtered:
            stacks = {k for k in stacks if filtered(k)}
        if costs == []:
            costs = {c.cost for c in stacks}
        stacks = filter(lambda c: c.cost in costs and stackNums[c] > 0, stacks)
        return itertools.combinations(stacks, number)
        
