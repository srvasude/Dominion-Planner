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
    
